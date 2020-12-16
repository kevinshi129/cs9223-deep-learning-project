import argparse
import os

import numpy as np
from PIL import Image, ImageEnhance

parser = argparse.ArgumentParser()

parser.add_argument('--im', type=str)
parser.add_argument('--save', type=str)

args = parser.parse_args()

if not os.path.exists(args.save):
    os.makedirs(args.save)

im = Image.open(args.im)

scales = [0.25, 0.5, 0.75, 1, 1.25, 1.5]

enhancer = ImageEnhance.Contrast(im)

for i, scale in enumerate(scales):
    im_out = enhancer.enhance(scale)
    im_out.save(os.path.join(args.save, str(i + 1) + '.png'))
