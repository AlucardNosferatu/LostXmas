import os

import cv2
import numpy as np
from cnocr import CnOcr
from tqdm import tqdm

from ocr_cutter_test import get_bounds, reduce_bounds, cut_bound, save_slices


def tag_by_bbox(model, filepath, str_list: list):
    img_array = cv2.imread(filepath)
    # xc_pic = img_array.shape[1] / 2
    out_this_slice = model.ocr(img_array)
    bbox_list = []
    slice_list = []
    for line_dict in out_this_slice:
        slice_list, bbox_list = line_dict_process(slice_list, img_array, line_dict, bbox_list)
    if len(slice_list) >= 2:
        if len(slice_list) >= 3:
            print('breakpoint')
        slice_list, bbox_list = sort_by_bbox(slice_list, bbox_list)
    str_list += slice_list
    return str_list


def line_dict_process(slice_list, img_array, line_dict, bbox_list):
    if len(line_dict['text']) <= 1:
        return slice_list
    else:
        tbc = tag_by_bcolor(img_array, line_dict['position'])
        text = line_dict['text'] + '\n'
        # x1 = line_dict['position'][0, 0]
        # x2 = line_dict['position'][2, 0]
        # xc_sen = (x1 + x2) / 2
        # if xc_sen < xc_pic:
        if tbc:
            text = 'a\t' + text
        else:
            text = 'q\t' + text
        slice_list.append(text)
        bbox_list.append(line_dict['position'])
        return slice_list, bbox_list


def sort_by_bbox(slice_list, bbox_list):
    def approximate(a_val, b_val):
        threshold = 5
        return abs(a_val - b_val) < threshold

    def prior_box(a_corner, b_corner):
        xa = a_corner[0]
        xb = b_corner[0]
        ya = a_corner[1]
        yb = b_corner[1]
        if not approximate(ya, yb):
            if ya > yb:
                return 'b'
            else:
                return 'a'
        else:
            if xa > xb:
                return 'b'
            else:
                return 'a'

    new_list = []
    new_bbox = []
    ref_index = 0
    cmp_index = 1
    # x_rc = corner[0]
    # y_rc = corner[1]
    while len(slice_list) > 0:
        if len(slice_list) == 1:
            new_list.append(slice_list.pop(ref_index))
            new_bbox.append(bbox_list.pop(ref_index))
        else:
            ref_box_corner = bbox_list[ref_index][0, :]
            cmp_box_corner = bbox_list[cmp_index][0, :]

            if prior_box(ref_box_corner, cmp_box_corner) == 'b':
                ref_index = cmp_index
            cmp_index += 1
            if cmp_index == len(slice_list):
                new_list.append(slice_list.pop(ref_index))
                new_bbox.append(bbox_list.pop(ref_index))
                ref_index = 0
                cmp_index = 1

    return new_list, bbox_list


def tag_by_bcolor(img_array, bbox):
    # bbox = line_dict['position']
    x1 = int(bbox[0, 0])
    y1 = int(bbox[0, 1])
    x2 = int(bbox[2, 0])
    y2 = int(bbox[2, 1])
    cropped_array = img_array[y1:y2, x1:x2, :]
    # cv2.imshow('cropped', cropped_array)
    # cv2.waitKey()
    histo = cv2.calcHist([cropped_array], [2], None, [256], [0, 256])[192:256, :]
    sum_histo = np.sum(histo)
    percent = sum_histo / (cropped_array.shape[0] * cropped_array.shape[1])
    return percent > 0.125


mdl = CnOcr(det_model_name='db_resnet34')
src_pics = os.listdir('pics')
for src_pic in src_pics:
    print('Now processing:', src_pic)
    # bl, img_arr = get_bounds(src_pic)
    # bl = reduce_bounds(bl)
    # sal = cut_bound(img_arr, bl)
    # save_slices(sal, src_pic)

    cut_dir = os.path.join('pics_cut', src_pic.strip('.jpg'))
    files = os.listdir(cut_dir)
    sl = []
    last_processed = -1
    for i in tqdm(range(len(files))):
        j = 0
        fp = ''
        while i + j - 1 <= last_processed or not os.path.exists(fp):
            fp = os.path.join(cut_dir, str(i + j) + '.jpg')
            j += 1
        sl = tag_by_bbox(mdl, fp, sl)
        last_processed = i + j - 1
    tgt_filepath = os.path.join('texts', src_pic.strip('.jpg') + '.txt')
    if os.path.exists(tgt_filepath):
        os.remove(tgt_filepath)
    with open(
            os.path.join(
                'texts',
                src_pic.strip('.jpg') + '.txt'
            ),
            mode='w',
            encoding='utf-8'
    ) as text_file:
        text_file.writelines(sl)
