import csv
from io import BytesIO, StringIO
from typing import Union

import requests
from PIL import Image

serial_number_column = "s"
product_name_column = "product"
input_image_urls_column = "urls"


def parse_csv(file):
    reader = csv.DictReader(StringIO(file.decode("utf-8")))
    image_data = []
    input_images = []
    for row in reader:
        serial_number = int(row[serial_number_column])
        product_name = row[product_name_column]
        input_image_urls = row[input_image_urls_column].split(",")
        image_data.append(
            {
                "serial_number": serial_number,
                "product_name": product_name,
                "input_image_urls": input_image_urls,
            },
        )
        input_images.extend(input_image_urls)
    return image_data, input_images


async def download_image(url: str) -> Union[bytes, None]:
    try:
        _image = requests.get(url)
        return _image.content
    except Exception as _:
        return None


async def compress_image(image_data: bytes, quality: int = 50) -> Union[bytes, None]:
    try:
        _image = Image.open(BytesIO(image_data))
        _output = BytesIO()
        _image.save(_output, format="JPEG", quality=quality)
        return _output.getvalue()
    except Exception as _:
        return None


def convert_dict_to_csv(data):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ["Serial Number", "Product Name", "Input Image URLs", "Output Image URLs"],
    )
    for item in data["image_data"]:
        input_urls = ", ".join(item["input_image_urls"])
        output_urls = ", ".join(item["output_image_urls"])
        writer.writerow(
            [item["serial_number"], item["product_name"], input_urls, output_urls],
        )
    output.seek(0)
    return output
