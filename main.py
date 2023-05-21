import pylibmagic
import pytesseract
from PIL import Image
from collections import Counter
import magic
import io
import os
import argparse

japan_ords = set(i for i in range(19969, 40959))

def frequency(text):
    return {k: v for k, v in Counter(text).most_common() if ord(k) in japan_ords}

def is_image(file):
    mime = magic.from_file(file, mime=True)
    return mime.startswith('image/')

def convert_to_png(file):
    image = Image.open(file)
    image = image.convert('RGBA')
    with io.BytesIO() as mem:
        image.save(mem, format='PNG')
        mem.seek(0)
        image_bytes = mem.read()
    return image_bytes

def extract_text(image, target_chars):
    target_kanji = ''.join(target_chars)
    text = pytesseract.image_to_string(image, config=f'--psm 11 --oem 2 -c tessedit_char_whitelist={target_kanji}', lang='jpn')
    return text

def main():
    parser = argparse.ArgumentParser(description='Simple Python program to read text from a file with .txt extension, generate an image with a caption, and save it as a .png file.')
    parser.add_argument('filename', help='Input filename')
    args = parser.parse_args()

    # Check if the input file has a .txt extension
    if not args.filename.lower().endswith('.txt'):
        print("Error: Input file must have a .txt extension.")
        return

    # Read text from input file
    with open(args.filename, 'r', encoding="utf-8") as file:
        text = file.read()

    source_kanji = set(ch for ch in text if ord(ch) in japan_ords)

    # Create the output filename with the same basename and .png extension
    basename = os.path.splitext(args.filename)[0]
    output_filename = f"{basename}.png"

    # Run the 'convert' command to generate the image with the caption
    command = f"convert -gravity center -size 600x -font '/System/Library/Fonts/Hiragino Sans GB.ttc' caption:'{text}' '{output_filename}'"
    os.system(command)

    image_bytes = convert_to_png(output_filename)
    image_png = Image.open(io.BytesIO(image_bytes))
    text = extract_text(image_png, source_kanji)
    kanji_text = set(ch for ch in text if ord(ch) in japan_ords)

    from pprint import pprint
    print("Input:\n", source_kanji)
    print("="*50)
    print("Recognised kanji:\n", kanji_text)

    print("-"*50)
    print("originally: {} \nrecognised: {}".format(len(source_kanji), len(kanji_text)))
    print("original kanji not recognised: {}".format(source_kanji -kanji_text))
    print("fake kanji by tesseract: {}".format(kanji_text - source_kanji))


if __name__ == '__main__':
    main()

