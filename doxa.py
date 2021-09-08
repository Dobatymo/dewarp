from PIL import Image, ImageDraw, ImageFont
import numpy as np
import doxapy
from doxapy import Binarization
import cv2

def read_image(file):
    return np.array(Image.open(file).convert("L"))

def binarize(grayscale_image, algo, args={}, inplace=False):

    if inplace:
        Binarization.update_to_binary(algo, grayscale_image, args)
    else:
        binary_image = np.empty(grayscale_image.shape, grayscale_image.dtype) # output image buffer

        binarization = Binarization(algo)
        binarization.initialize(grayscale_image)
        binarization.to_binary(binary_image, args)

        return binary_image

def adaptive_otsu(path, blur=True, blockx=64, blocky=64, magic=0.74, out=None):

    """ based on:
        Fast Document Image Binarization Based on an Improved Adaptive Otsu's Method and Destination Word Accumulation
    """

    from genutility.numpy import unblock2d, block2d, unblock

    img = cv2.imread(path, 0)
    a = img.shape[0] // blockx
    b = img.shape[1] // blocky

    blocks = unblock2d(img, blockx, blocky, blocksize=True)
    assert np.array_equal(blocks, unblock(img, blockx, blocky, blocksize=True))

    if out is None:
        out = np.empty(blocks.shape, dtype=bool)

    for i in range(blocks.shape[0]):
        
        block_original = blocks[i]
        
        if blur:
            block_processed = cv2.GaussianBlur(block_original, (5,5), 0)
        else:
            block_processed = block_original

        thresh, fn_min = adaptive_otsu_block(block_processed)
        if fn_min > magic:
            block_binary = np.where(block_original < thresh, False, True)
        else:
            block_binary = np.ones(block_original.shape, dtype=bool)
        
        out[i] = block_binary
    
    return block2d(out, a, b, blockx, blocky)

def adaptive_otsu_block(block):
    hist = cv2.calcHist([block], [0], None, [256], [0, 256])
    hist_norm = hist.ravel()/hist.sum()
    Q = hist_norm.cumsum()
    bins = np.arange(256)

    fn_min = np.inf
    thresh = -1

    for i in range(1, 256):
        p1, p2 = np.hsplit(hist_norm, [i]) # probabilities
        q1, q2 = Q[i], Q[255] - Q[i] # cum sum of classes
        if q1 < 1.e-6 or q2 < 1.e-6:
            continue

        b1, b2 = np.hsplit(bins,[i]) # weights
        # finding means and variances
        m1, m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
        v1, v2 = np.sum(((b1-m1)**2)*p1)/q1, np.sum(((b2-m2)**2)*p2)/q2

        fn = v1*q1 + v2*q2
        if fn < fn_min:
            fn_min = fn
            thresh = i

    return thresh, fn_min

def test_doxa(path):
    font = ImageFont.truetype("arial.ttf", 36)
    grayscale_image = read_image(path)

    for algo, args in [
            (Binarization.Algorithms.OTSU, {}),
            (Binarization.Algorithms.BERNSEN, {}),
            (Binarization.Algorithms.NIBLACK, {}),
            (Binarization.Algorithms.SAUVOLA, {}),
            (Binarization.Algorithms.WOLF, {}),
            (Binarization.Algorithms.NICK, {}),
            (Binarization.Algorithms.SU, {}),
            (Binarization.Algorithms.TRSINGH, {}),
            (Binarization.Algorithms.BATAINEH, {}),
            (Binarization.Algorithms.ISAUVOLA, {}),
            (Binarization.Algorithms.WAN, {}),
            (Binarization.Algorithms.GATOS, {}),
        ]:
        binary_image = binarize(grayscale_image, algo, args)
        # Display our resulting image
        img = Image.fromarray(binary_image)

        draw = ImageDraw.Draw(img)
        draw.text((0, 0), str(algo), color=0, font=font)
        
        img.show()

if __name__ == "__main__":
    path = "output-linear-512x512.png"

    #test_doxa(path)
    for size in (16, 32, 64, 128):
        img = adaptive_otsu(path, blur=False, blockx=size, blocky=size)
        Image.fromarray(img).save(f"adaptive-otsu_{size}.png")
