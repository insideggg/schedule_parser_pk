import requests
from PIL import Image
from io import BytesIO

def resize_image(image_url, max_width, max_height):
    response = requests.get(image_url)
    response.raise_for_status()

    img = Image.open(BytesIO(response.content))

    original_width, original_height = img.size
    aspect_ratio = original_width / original_height

    if original_width > original_height:
        new_width = min(max_width, original_width)
        new_height = int(new_width / aspect_ratio)
        if new_height > max_height:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        new_height = min(max_height, original_height)
        new_width = int(new_height * aspect_ratio)
        if new_width > max_width:
            new_width = max_width
            new_height = int(new_width * aspect_ratio)

    return [new_width, new_height]
