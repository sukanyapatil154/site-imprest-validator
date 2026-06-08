import easyocr
import re

reader = easyocr.Reader(['en'])

def get_amount_from_image(image_path):

    results = reader.readtext(image_path)

    text = " ".join([r[1] for r in results])

    amounts = re.findall(
        r'\d+\.\d+|\d+',
        text
    )

    amounts = [float(x) for x in amounts]

    if len(amounts) == 0:
        return 0

    return max(amounts)
