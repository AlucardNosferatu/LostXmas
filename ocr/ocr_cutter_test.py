import os.path

import cv2
import numpy as np
from tqdm import tqdm

# img_fp = 'test.jpg'
img_fn = 'xiaoice_island (1).jpg'


def get_bounds(img_filename):
    img_filepath = os.path.join('pics', img_filename)
    img_array = cv2.imread(img_filepath)
    scan_position_horizon_1 = int(img_array.shape[1] / 6)
    scan_position_horizon_2 = scan_position_horizon_1 * 5
    scan_position_horizon_1 += 30
    scan_position_horizon_2 -= 30

    temp_color_1 = np.array([0, 0, 0])
    temp_color_2 = np.array([0, 0, 0])
    color_target_1 = np.array([255, 255, 255])
    color_target_2 = np.array([254, 236, 143])
    detected = False
    bound_lines = []
    for i in tqdm(range(img_array.shape[0])):
        color_sampled_1 = img_array[i, scan_position_horizon_1, :].copy()
        color_sampled_2 = img_array[i, scan_position_horizon_2, :].copy()
        if i != 0:
            if (color_sampled_1 != temp_color_1).all() or (color_sampled_2 != temp_color_2).all():
                diff1_1 = np.sum(np.square(color_target_1 - color_sampled_1))
                diff1_2 = np.sum(np.square(color_target_1 - temp_color_1))
                diff2_1 = np.sum(np.square(color_target_2 - color_sampled_2))
                diff2_2 = np.sum(np.square(color_target_2 - temp_color_2))
                diff1_3 = np.sum(np.square(temp_color_1 - color_sampled_1))
                diff2_3 = np.sum(np.square(temp_color_2 - color_sampled_2))
                if (diff1_3 > 10 and diff1_1 + diff1_2 < 1000) or (diff2_3 > 10 and diff2_1 + diff2_2 < 1000):
                    detected = True
                    # print('========================')
                    # print(i)
                    # print(temp_color_1, temp_color_2)
                    # print(color_sampled_1, color_sampled_2)
                    # print(diff1_1, diff1_2, diff2_1, diff2_2)
        temp_color_1 = color_sampled_1.copy()
        temp_color_2 = color_sampled_2.copy()
        if detected:
            bound_lines.append(i)
            detected = False

    return bound_lines, img_array


def reduce_bounds(bound_lines):
    prev_bound = 0
    blacklist = []
    for i in range(len(bound_lines)):
        distance = bound_lines[i] - prev_bound
        if distance < 75:
            blacklist.append(i)
        prev_bound = bound_lines[i]
    while len(blacklist) > 0:
        print('Removed:', bound_lines.pop(blacklist.pop(-1)))
    return bound_lines


def display_bound(img_array, bound_lines):
    displayed_array = img_array.copy()
    for bound_line in bound_lines:
        displayed_array[bound_line, :, 0] = 255
        displayed_array[bound_line, :, 1] = 0
        displayed_array[bound_line, :, 2] = 0
    x = displayed_array.shape[0]
    y = displayed_array.shape[1]
    cv2.imshow('bound_lines', cv2.resize(displayed_array, (int(y / 3), int(x / 3))))
    cv2.waitKey()


def cut_bound(img_array, bound_lines):
    slice_array_list = []
    upper_bound = 0
    for i in tqdm(range(len(bound_lines))):
        lower_bound = bound_lines[i]
        slice_array = img_array[upper_bound:lower_bound, :, :].copy()
        slice_array_list.append(slice_array)
        # cv2.imshow('bound_lines', slice_array)
        # cv2.waitKey()
        upper_bound = lower_bound
    slice_array = img_array[upper_bound:, :, :].copy()
    slice_array_list.append(slice_array)
    # cv2.imshow('bound_lines', slice_array)
    # cv2.waitKey()
    return slice_array_list


def save_slices(slice_array_list, img_filename):
    save_dir = os.path.join('pics_cut', img_filename.strip('.jpg'))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for index, slice_array in tqdm(enumerate(slice_array_list)):
        cv2.imwrite(os.path.join(save_dir, str(index) + '.jpg'), slice_array)


if __name__ == '__main__':
    bl, img_arr = get_bounds(img_fn)
    bl = reduce_bounds(bl)
    sal = cut_bound(img_arr, bl)
    save_slices(sal, img_fn)
