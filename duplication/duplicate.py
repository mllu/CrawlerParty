import sys
import os
import io
import hashlib
import distance
from PIL import Image

__author__ = 'Taichi1'

hammingDistanceThreshold = 4


def calculate_hamming_distance(hash1, hash2):
    return distance.hamming(hash1, hash2)


def is_exact_duplicate(image_file1_name, image_file2_name):
    imageFile1 = open(image_file1_name).read()
    imageFile2 = open(image_file2_name).read()

    image1Hash = hashlib.md5(imageFile1).hexdigest()
    image2Hash = hashlib.md5(imageFile2).hexdigest()

    return image1Hash == image2Hash


def is_near_duplicate(image_file1_name, image_file2_name):
    return calculate_hamming_distance(dhash(Image.open(image_file1_name)),
                                      dhash(Image.open(image_file2_name))) \
           < hammingDistanceThreshold


def md5hash(imageFile):
    img = Image.open(imageFile)
    m = hashlib.md5()
    with io.BytesIO() as memf:
        img.save(memf, 'PNG')
        data = memf.getvalue()
        m.update(data)
        return m.hexdigsest()


# dhash implementation. It doesn't work very well. It seems to group all pictures with similar background into a same
# near duplicate group
# Reference: http://blog.iconfinder.com/detecting-duplicate-images-using-python/
# Licensed: Free to Use

def dhash(image, hash_size=8):
    # Step 1 and 2: Greyscale and then resize.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixelList = list(image.getdata())

    # Step 3: Compare the adjacent pixels.
    difference = []
    for row in range(0, hash_size):
        for col in range(0, hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Step 4: Convert the binary array to a hexadecimal string.
    decimal_value = 0
    # hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
    # strip the 0x prefix of a hex string
    hexValue = hex(decimal_value)[2:].rjust(2, "0")

    return hexValue


def hashfunc(image_file_name, hash_method):
    image = Image.open(image_file_name)
    try:
        image.load()
    except IOError:
        pass  # You can always log it to logger

    if hash_method == "dhash":
        return dhash(image)
    elif hash_method == "averageHash":
        return averageHash(image)


# actually this works pretty good, better than the dhash in this case. Since what we want to do is to detect some resize
# of the picture. So this average approach works great
# Reference: https://www.safaribooksonline.com/blog/2013/11/26/image-hashing-with-python/
def averageHash(image_file_name):
    image = image_file_name.convert('L'). \
        resize((8, 8), Image.ANTIALIAS)  # Reduce it's size.
    # image = image_file_name.convert('L')  # Convert it to grayscale.
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))  # '00010100...'
    hexadecimal = int(bits, 2).__format__('016x').upper()
    return hexadecimal


# it seems quite complicated. For now, leave it alone
# Reference: http://www.hackerfactor.com/blog/?/archives/432-Looks-Like-It.html
def phash(image_file_name):
    return "000000000000"


def find_similar(userpath, is_exact="False"):
    def list_path_and_add_file(toAddlist, path):
        if os.path.isdir(path) and ".idea" not in path:
            for childpath in os.listdir(path):
                list_path_and_add_file(toAddlist, os.path.join(path, childpath))
        elif not os.path.isdir(path):
            if "DS_Store" not in path:
                toAddlist.append(path)

    hash_method = "averageHash"
    # hash_method = "dhash"
    pathlist = []
    list_path_and_add_file(pathlist, userpath)
    # image_filenames = [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
    images = {}
    # print(is_exact)
    print("Number of photos before duplication: ", len(pathlist))
    i = 0
    for img in sorted(pathlist):
        # print(img)
        i += 1
        if i % 10000 == 0:
            print("process", i)
        if is_exact.lower() == "true":
            # print("Exact Duplicate")
            hashValue = md5hash(img)
        else:
            # print("Near Duplicate")
            hashValue = hashfunc(img, hash_method)
        images[hashValue] = images.get(hashValue, []) + [img]
    for k, img_list in images.items():
        if len(img_list) > 1:
            print(" ".join(img_list))
    print("Number of photos before duplication: ", len(pathlist))
    print("Number of photos after duplication: ", len(images))


if __name__ == '__main__':
    def usage():
        sys.stderr.write("""SYNOPSIS: python %s <directory> [<is_exact>]\n""" % sys.argv[0])
        sys.exit(1)


    userpath = sys.argv[1] if len(sys.argv) > 1 else usage()
    is_exact = sys.argv[2] if len(sys.argv) > 1 else "false"
    find_similar(userpath=userpath, is_exact=is_exact)
