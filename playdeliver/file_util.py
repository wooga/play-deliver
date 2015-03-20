"""module with utility functions for the file system."""

import os
import errno


def list_dir_abspath(path):
    """
    Return a list absolute file paths.

    see mkdir_p os.listdir.
    """
    return map(lambda f: os.path.join(path, f), os.listdir(path))


def mkdir_p(path):
    """Create a new directory with with all missing folders in between."""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
