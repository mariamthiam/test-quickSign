import asyncio
from typing import List, ByteString
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
import urllib.request
import hashlib
import io
from mongoengine import connect, errors
from image_tables import ImageHandler, ImageStatus
from pymongo import MongoClient, collection


def get_db_collection(collection_name: str) -> collection.Collection:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["images"]
    return db[collection_name]


def connect_mongo_imgs_db():
    connect('images', host='localhost', port=27017)


def image_to_binary(image: JpegImageFile) -> ByteString:
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        return output.getvalue()


def binary_to_image(image_bin: ByteString) -> JpegImageFile:
    return Image.open(io.BytesIO(image_bin))


async def getImageFromURL(url: str) -> JpegImageFile:
    image = Image.open(urllib.request.urlopen(url))
    if not image:
        raise FileNotFoundError(f"Can not found image at url {url}")
    return image


def readUrlsInFile(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return file.read().split("\n")


async def getImageMD5(img: JpegImageFile)-> str:
    return hashlib.md5(img.tobytes()).hexdigest()


async def getImageToBlackWhite(img: JpegImageFile) -> JpegImageFile:
    grey_img = img.copy()
    (width, height) = grey_img.size
    for x in range(width):
        for y in range(height):
            (R, G, B) = img.getpixel((x, y))
            grey_color = int((R+G+B)/3)
            grey_img.putpixel((x, y), (grey_color, grey_color, grey_color))
    return grey_img


async def saveImageInMongo(url):
    try:
        img = await getImageFromURL(url)
        [md5, grey_img] = await asyncio.gather(
            *[
                getImageMD5(img),
                getImageToBlackWhite(img)
            ]
        )
        width, height = img.size
        image_to_save = ImageHandler(
            md5=md5,
            original_image=image_to_binary(img),
            grey_image=image_to_binary(grey_img),
            width=width,
            height=height
        )
        image_to_save.save()
        ImageStatus(
            url=url
        ).save()
    except errors.NotUniqueError:
        pass
    except Exception as e:
        try:
            ImageStatus(
                url=url,
                with_error=True
            ).save()
            print(e)
        except errors.NotUniqueError:
            pass


if __name__ == "__main__":
    urls = readUrlsInFile("urls.txt")
    loop = asyncio.get_event_loop()
    connect_mongo_imgs_db()
    loop.run_until_complete(
        asyncio.wait(
            [
                saveImageInMongo(url) for url in urls
            ]
        )
    )
