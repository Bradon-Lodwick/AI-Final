#!/usr/bin/env python
""" This file contains all of the image file manipulation functions, such as creating images from a matrix.

TODO
----
*

"""

__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"


import imageio
import os
import glob
from enum import Enum, unique


@unique
class SortMethod(Enum):
    """ The type of sorting to use.

    """

    ALPHABETICAL = 0  # Used to sort a list alphabetically
    DATE = 1  # Used to sort a list by the date of files created (works only with lists of files)


def create_gif(folder_path, frame_time=0.1, file_type="png", output="output", sort_type=SortMethod.DATE):
    """ Creates a gif of all of the image files inside the folder of the given file type.
    The gif will be created by taking a list of names in the given folder.

    Parameters
    ----------
    folder_path : str
        The path to the folder of the image files.
    frame_time : float
        The number of seconds each frame should be visible for.
        Defaults to a tenth of a second.
    file_type : str
        The type of the file to check for in the given folder. Do not input the . when giving the file type.
        Defaults to png files.
    output : str
        The name of the gif to be output.  The .gif extension is added automatically.
    sort_type : SortMethod
        The desired way to sort the list of files before creating the gif (order of frames).
        Defaults to using alphabetical sorting.

    Raises
    ------
    IOError:
        Raised if a given path does not exist, or if the given path doesn't have any files of the given type.

    """

    # Checks first to see if the given folder exists
    if not os.path.exists(folder_path):
        raise IOError("The given path ({0}) does not exist.".format(folder_path))

    # Gets a list of the frames
    file_list = glob.glob(folder_path + os.sep + "*." + file_type)  # Gets the list of files

    # Checks to make sure there is at least 1 valid file in the given folder to create the gif with
    if len(file_list) == 0:
        raise IOError("There are no images in the given folder with a type of {0}".format(file_type))

    # Sorts the list by the given sort type
    if sort_type == SortMethod.ALPHABETICAL:
        pass  # TODO
    elif sort_type == SortMethod.DATE:
        file_list.sort(key=os.path.getmtime)


if __name__ == "__main__":
    create_gif("test_data", output="test1")
    pass
