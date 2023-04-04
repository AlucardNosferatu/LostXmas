import os

import cv2
from cnocr import CnOcr
from tqdm import tqdm

from ocr_cutter_test import get_bounds, reduce_bounds, cut_bound, save_slices


def tag_by_bbox(model, filepath, str_list: list):
    img_array = cv2.imread(filepath)
    xc_pic = img_array.shape[1] / 2
    out_this_slice = model.ocr(img_array)
    for line_dict in out_this_slice:
        if len(line_dict['text']) <= 1:
            continue
        else:
            text = line_dict['text'] + '\n'
            x1 = line_dict['position'][0, 0]
            x2 = line_dict['position'][1, 0]
            xc_sen = (x1 + x2) / 2
            if xc_sen < xc_pic:
                text = 'a\t' + text
            else:
                text = 'q\t' + text
            str_list.append(text)
    return str_list


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
