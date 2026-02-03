import argparse
import logging
import numpy as np
import os
import re
import sys
import traceback
from typing import List, Dict, Tuple

from PIL import Image
from idc.core import ENV_IDC_LOGLEVEL
from seppl.io import locate_files
from wai.logging import add_logging_level, init_logging, set_logging_level

LAYER_SEGMENTS = "idc-layer-segments"

_logger = logging.getLogger(LAYER_SEGMENTS)


BASE_AUGMENTATION_NONE = "none"
BASE_AUGMENTATION_GRAYSCALE_STRETCH = "grayscale-stretch"
BASE_AUGMENTATIONS = [
    BASE_AUGMENTATION_NONE,
    BASE_AUGMENTATION_GRAYSCALE_STRETCH,
]


def assemble_names(imgs: List[str], img_match: str, img_format: str) -> Dict[str, str]:
    """
    Generates the new name for each of the files and returns a dictionary (full path -> new name excl path).

    :param imgs: the images to process
    :type imgs: list
    :param img_match: the regexp for extracting the groups
    :type img_match: str
    :param img_format: the template for assembling the new name from the groups
    :type img_format: str
    :return: the dictionary of full path / new name
    :rtype: dict
    """
    result = dict()

    for img in imgs:
        name = os.path.splitext(os.path.basename(img))[0]
        match = re.search(img_match, name)
        if match is None:
            _logger.warning("Expression '%s' extracted no groups from: %s" % (img_match, name))
            continue
        name_new = img_format
        for i in range(1, match.lastindex+1):
            name_new = name_new.replace("{%d}" % i, match.group(i))
        _logger.debug("%s\n  --> %s" % (img, name_new))
        result[img] = name_new

    return result


def match(base_imgs: Dict[str, str], ann_imgs: Dict[str, str]) -> Dict[str, Tuple[str, List[str]]]:
    """
    Matches the base and annotation images.

    :param base_imgs: the base images dictionary (full path -> new name)
    :type base_imgs: dict
    :param ann_imgs: the annotation images dictionary (full path -> new name)
    :return: the generated dictionary of: new name -> (base img, [ann imgs])
    :rtype: dict
    """
    result = dict()

    # set up data structure with base images
    for img in base_imgs:
        result[base_imgs[img]] = (img, list())

    # attach annotations
    for img in ann_imgs:
        if ann_imgs[img] in result:
            result[ann_imgs[img]][1].append(img)

    # remove any entries with no annotations
    empty = []
    for k in result:
        if len(result[k][1]) == 0:
            empty.append(k)
    if len(empty) > 0:
        _logger.info("Removing # entries with no matching annotations: %d" % len(empty))
        for k in empty:
            result.pop(k)

    return result


def generate_output(base: str, anns: List[str], name: str, output: str, base_aug: str = BASE_AUGMENTATION_NONE,
                    suffix: str = "-object-", dry_run: bool = False):
    """
    Generates output from the base image and its annotations in the output directory, using the new name.

    :param base: the base image to use
    :type base: str
    :param anns: the annotation images to use
    :type anns: list
    :param name: the new name to use for the output (no ext)
    :type name: str
    :param output: the output directory to store the results in
    :type output: str
    :param base_aug: the augmentation to apply to the base image
    :type base_aug: str
    :param suffix: the suffix to use for the layer segments, 1-based index gets automatically appended
    :type suffix: str
    :param dry_run: whether to only simulate the processing
    :type dry_run: bool
    """
    # base image
    base_out = os.path.join(output, name + ".jpg")
    base_img = Image.open(base)
    if base_aug == BASE_AUGMENTATION_NONE:
        pass
    elif base_aug == BASE_AUGMENTATION_GRAYSCALE_STRETCH:
        arr = np.array(base_img)
        amin = arr.min()
        amax = arr.max()
        if amax > amin:
            arr_norm = (arr - amin) / (amax - amin)
        else:
            arr_norm = arr * 0
        arr_u8 = (255 * arr_norm).astype(np.uint8)
        base_img = Image.fromarray(arr_u8)
    else:
        raise Exception("Unhandled base image augmentation: %s" % base_aug)
    _logger.info("Writing base image: %s" % base_out)
    if not dry_run:
        base_img.save(base_out)

    # annotations
    for i, ann in enumerate(anns, start=1):
        img = Image.open(ann)
        arr = np.array(img)
        arr = np.where(arr > 0, 255, 0).astype(np.uint8)
        ann_img = Image.fromarray(arr, "L").convert("1")
        ann_out = os.path.join(output, name + suffix + str(i) + ".png")
        _logger.info("Writing annotation: %s" % ann_out)
        if not dry_run:
            ann_img.save(ann_out)


def generate(base: List[str], ann: List[str], output: str,
             base_match: str = "(.*)", base_format: str = "{1}", base_aug: str = BASE_AUGMENTATION_NONE,
             ann_match: str = "(.*)", ann_format: str = "{1}",
             suffix: str = "-object-", dry_run: bool = False):
    """
    Generates instance PNGs from the base and annotation images.

    :param base: the dir(s) to look for base images, supports glob
    :type base: list
    :param ann: the dir(s) to look for annotation images, supports glob
    :type ann: list
    :param output: the directory to store the generated pairs (base image and annotation)
    :type output: str
    :param base_match: the regexp with groups for extracting the new base image name
    :type base_match: str
    :param base_format: the format for combining the extracted groups to form the new base image name, no ext, group placeholder {X} with X=1,2,...
    :type base_format: str
    :param base_aug: the augmentation to perform on the base image
    :type base_aug: str
    :param ann_match: the regexp with groups for extracting the new annotation image name
    :type ann_match: str
    :param ann_format: the format for combining the extracted groups to form the new annotation image name, no ext, group placeholder {X} with X=1,2,...
    :type ann_format: str
    :param suffix: the suffix to use for the layer segments, 1-based index gets automatically appended
    :type suffix: str
    :param dry_run: whether to only simulate the processing
    :type dry_run: bool
    """
    base_imgs = locate_files(base, fail_if_empty=False)
    _logger.info("# base images found: %d" % len(base_imgs))
    base_imgs = assemble_names(base_imgs, base_match, base_format)

    ann_imgs = locate_files(ann, fail_if_empty=False)
    _logger.info("# annotation images found: %d" % len(ann_imgs))
    ann_imgs = assemble_names(ann_imgs, ann_match, ann_format)

    matches = match(base_imgs, ann_imgs)
    _logger.info("Found # matches: %d" % len(matches))
    max_ann = 0
    for name in matches:
        max_ann = max(max_ann, len(matches[name][1]))
    _logger.info("Max # of annotations encountered: %d" % max_ann)

    for name in matches:
        generate_output(matches[name][0], matches[name][1], name, output, base_aug=base_aug,
                        suffix=suffix, dry_run=dry_run)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_IDC_LOGLEVEL)
    parser = argparse.ArgumentParser(prog=LAYER_SEGMENTS, description="Creates layer segments annotations from PNG files with individual annotations. Each individual annotation will get a different suffix.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--base_input", metavar="DIR", help="The dir(s) to scan for image files that form the base image for the annotations; glob syntax is supported.", default=None, type=str, required=True, nargs="+")
    parser.add_argument("-m", "--base_match", metavar="REGEXP", help="The regular expression group(s) to use for extracting the new base name for the image (extension is removed before matching).", default="(.*)", type=str, required=False)
    parser.add_argument("-g", "--base_format", metavar="REGEXP", help="The name format to use for constructing the new base name from the groups (no extension; group placeholder: {X} with X being group 1, 2, etc).", default="{1}", type=str, required=False)
    parser.add_argument("-a", "--base_aug", choices=BASE_AUGMENTATIONS, help="The augmentation to apply to the base image", default=BASE_AUGMENTATION_NONE, type=str, required=False)
    parser.add_argument("-I", "--annotations_input", metavar="DIR", help="The dirs(s) to scan for image files that make up the annotations; glob syntax is supported.", default=None, type=str, required=True, nargs="+")
    parser.add_argument("-M", "--annotations_match", metavar="REGEXP", help="The regular expression group(s) to use for extracting the new annotation name for the image (extension is removed before matching).", default="(.*)", type=str, required=False)
    parser.add_argument("-G", "--annotations_format", metavar="REGEXP", help="The name format to use for constructing the new annotation name from the groups (no extension; group placeholder: {X} with X being group 1, 2, etc).", default="{1}", type=str, required=False)
    parser.add_argument("-s", "--suffix", metavar="SUFFIX", help="The suffix to use for the layers, 1-based indexed gets automatically appended.", default="-object-", type=str, required=False)
    parser.add_argument("-o", "--output", metavar="DIR", help="The directory to store the cleaned up base image and annotations in.", default=None, type=str, required=True)
    parser.add_argument("-n", "--dry_run", action="store_true", help="Whether to only simulate the generation.")
    add_logging_level(parser)
    parsed = parser.parse_args(args=args)
    set_logging_level(_logger, parsed.logging_level)
    generate(parsed.base_input, parsed.annotations_input, parsed.output,
             base_match=parsed.base_match, base_format=parsed.base_format, base_aug=parsed.base_aug,
             ann_match=parsed.annotations_match, ann_format=parsed.annotations_format,
             suffix=parsed.suffix, dry_run=parsed.dry_run)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        traceback.print_exc()
        print("options: %s" % str(sys.argv[1:]), file=sys.stderr)
        return 1


if __name__ == '__main__':
    main()
