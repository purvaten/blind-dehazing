import cv2
import cPickle
import logging
import os
import random
import sys
import yaml
import numpy as np
import time

from bunch import bunchify

# Our module imports
import steps

from config.arguments import parser
import tools


logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def save(img_file, patches, pairs):
    with open(img_file.split('.')[0] + '.patches', 'wb') as f:
        cPickle.dump(patches, f)
    with open(img_file.split('.')[0] + '.pairs', 'wb') as f:
        cPickle.dump(pairs, f)


def load(img_file):
    if not os.path.exists(img_file.split('.')[0] + '.patches'):
        return None, None
    with open(img_file.split('.')[0] + '.patches', 'rb') as f:
        patches = cPickle.load(f)
    with open(img_file.split('.')[0] + '.pairs', 'rb') as f:
        pairs = cPickle.load(f)
    return patches, pairs


def main():
    args = parser.parse_args()
    with open(args.constants, 'r') as f:
        constants = bunchify(yaml.load(f))

    logger.info("Loading image %s ..." % args.input)
    img = cv2.imread(args.input, flags=cv2.IMREAD_COLOR)
    # image scaled in 0-1 range
    img = img / 255.0
    # Scale array must be in decreasing order
    # scaled_imgs = steps.scale(img, [1, 0.75, 0.5, 0.375, 0.3, 0.25])
    scaled_imgs = steps.scale(img, [1, 300.0 / 384, 200.0 / 384, 150.0 / 384, 120.0 / 384, 100.0 / 384])

    if not args.no_cache:
        patches, pairs = load(args.input)
    else:
        patches, pairs = None, None
    if patches is None and pairs is None:
        logger.info("Extracting patches ...")
        patches = steps.generate_patches(scaled_imgs, constants)

        logger.info("Generating pairs of patches ...")
        pairs = steps.generate_pairs(patches, constants)

        logger.info("Removing duplicates ...")
        pairs = steps.remove_duplicates(pairs)

        logger.info("Saving patches and pairs ...")
        save(args.input, patches, pairs)
    else:
        logger.info("Using saved patches and pairs ...")

    logger.info("Filtering pairs of patches and estimating local airlight ...")
    pairs = steps.filter_pairs(patches, pairs, constants)

    pairs2 = steps.remove_overlaps(pairs, constants)

    # k = 547
    # p1 = pairs2[k]
    # stats = []

    # for i, p2 in enumerate(pairs2):
    #     if i == k:
    #         continue
    #     if p2.first == p1.first:
    #         stats.append(p2.second)
    #     elif p2.second == p1.first:
    #         stats.append(p2.first)

    # sum1 = np.zeros((len(pairs), 3))
    # for i, pair in enumerate(pairs2):
    #     sum1[i] = pair.airlight
    # print np.mean(sum1, axis=0)

    logger.info("Removing outliers ...")
    pairs2 = steps.remove_outliers(pairs2, constants)

    logger.info("Estimating global airlight ...")
    airlight = steps.estimate_airlight(pairs)

    logger.info("Estimatied airlight is ...")

if __name__ == '__main__':
    main()
