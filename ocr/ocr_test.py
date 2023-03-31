from cnocr import CnOcr

ocr = CnOcr(det_model_name='db_resnet34')
img_fp = 'pics/xiaoice_island (15).jpg'
out = ocr.ocr(img_fp)
print("Predicted Chars:", out)
