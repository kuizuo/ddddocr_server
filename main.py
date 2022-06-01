import time
import ddddocr
import uvicorn
import argparse
import base64
from fastapi import FastAPI, Form, File, UploadFile

from pydantic import BaseModel

parser = argparse.ArgumentParser(description="使用ddddocr搭建的最简api服务")
parser.add_argument("-p", "--port", type=int, default=8124)
args = parser.parse_args()


class Ocr():
    ocr = ddddocr.DdddOcr()
    det = ddddocr.DdddOcr(det=True)
    slide = ddddocr.DdddOcr(det=False, ocr=False)

    @staticmethod
    def code_image(img: bytes):
        return Ocr.ocr.classification(img)

    @staticmethod
    def det_image(img: bytes):
        return Ocr.det.detection(img)

    @staticmethod
    def slide_image(target_img: bytes, background_img: bytes):
        try:
            return Ocr.slide.slide_comparison(target_img, background_img)
        except Exception as e:
            return Ocr.slide.slide_match(target_img, background_img)


def ocr_img(type, img_bytes, background_img_bytes):
    if type == 1:
        return Ocr.code_image(img_bytes)
    elif type == 2:
        return Ocr.det_image(img_bytes)
    elif type == 3:
        return Ocr.slide_image(
            img_bytes, background_img_bytes)
    else:
        return None


app = FastAPI()


class Item(BaseModel):
    type: int = 1  # 1英数 2点选 3滑块
    img: str
    backgroundImg: str = None  # 滑块背景


@app.post("/ocr")
async def ocr_image(item: Item):
    """ 识别Base64编码图片 """
    try:
        type = item.type
        img_bytes = base64.b64decode(item.img, altchars=None, validate=False)
        background_img_bytes = bytes()
        if item.backgroundImg is not None:
            background_img_bytes = base64.b64decode(
                item.backgroundImg, altchars=None, validate=False)

        t = time.perf_counter()

        result = ocr_img(type, img_bytes, background_img_bytes)

        return {'code': 1, 'result': result, 'consumeTime': int((time.perf_counter() - t)*1000), 'msg': 'success'}
    except Exception as e:
        return {'code': 0, 'result': None, 'msg': str(e).strip()}


@app.post("/ocr/file")
async def ocr_image_file(type: int = Form(1), img: UploadFile = File(None), backgroundImg: UploadFile = File(None)):
    """ 识别文件上传图片 """
    try:
        img_bytes = await img.read()
        background_img_bytes = bytes()
        if backgroundImg is not None:
            background_img_bytes = await backgroundImg.read()

        t = time.perf_counter()
        result = ocr_img(type, img_bytes, background_img_bytes)

        return {'code': 1, 'result': result, 'consumeTime': int((time.perf_counter() - t)*1000), 'msg': 'success'}
    except Exception as e:
        return {'code': 0, 'result': None, 'msg': str(e).strip()}


@app.get("/ping")
def ping():
    return "pong"


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0",
                port=args.port, reload=True, debug=True)
