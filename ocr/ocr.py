import os

from cnocr import CnOcr
from tqdm import tqdm

from ocr_cutter_test import get_bounds, reduce_bounds, cut_bound, save_slices

model = CnOcr(det_model_name='db_resnet34')
src_pics = os.listdir('pics')
for src_pic in src_pics:
    print('Now processing:', src_pic)
    # bl, img_arr = get_bounds(src_pic)
    # bl = reduce_bounds(bl)
    # sal = cut_bound(img_arr, bl)
    # save_slices(sal, src_pic)

    cut_dir = os.path.join('pics_cut', src_pic.strip('.jpg'))
    files = os.listdir(cut_dir)
    str_list = []
    for i in tqdm(range(len(files))):
        filepath = os.path.join(cut_dir, str(i) + '.jpg')
        out = model.ocr(filepath)
        str_list += [line_dict['text'] + '\n' for line_dict in out]
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
        text_file.writelines(str_list)
