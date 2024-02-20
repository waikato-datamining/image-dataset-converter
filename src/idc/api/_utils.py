import os
from typing import Optional, Union, List


def locate_file(path: str, ext: Union[str, List[str]], rel_path: str = None) -> List[str]:
    """
    Tries to locate the associate files for the given path by replacing its extension by the provided ones.

    :param path: the base path to use
    :type path: str
    :param ext: the extension(s) to look for (incl dot)
    :type ext: str or list
    :param rel_path: the relative path to the annotation to use for looking for associated files, ignored if None
    :type rel_path: str
    :return: the located files
    :rtype: list
    """
    result = []
    if rel_path is not None:
        parent_path = os.path.dirname(path)
        name = os.path.basename(path)
        path = os.path.join(parent_path, rel_path, name)
    noext = os.path.splitext(path)[0]
    for current in ext:
        path = noext + current
        if os.path.exists(path):
            result.append(path)
    return result


def locate_image(path: str, rel_path: str = None) -> Optional[str]:
    """
    Tries to locate the image (png or jpg) for the given path by replacing its extension.

    :param path: the base path to use
    :type path: str
    :param rel_path: the relative path to the annotation to use for looking for images, ignored if None
    :type rel_path: str
    :return: the located image, None if not found
    :rtype: str
    """
    ext = [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"]
    images = locate_file(path, ext, rel_path=rel_path)
    if len(images) == 0:
        return None
    else:
        return images[0]
