import os
import tempfile
from pathlib import Path

import cloudfspy
from .utils import rm_tree, ls_tree

CACHE_FOLDER_ENV_VAR_NAME = cloudfspy.__name__.upper() + "_CACHE"


def set_cache_folder(folder: str):
    """
    Set the cache folder.
    :param folder: The folder to set.
    """
    os.environ[CACHE_FOLDER_ENV_VAR_NAME] = folder


def get_cache_folder() -> Path:
    """
    Get the cache folder.
    :return: The cache folder.
    """
    default_location = Path(tempfile.gettempdir()).joinpath(f".{cloudfspy.__name__}")
    folder = Path(os.environ.get(CACHE_FOLDER_ENV_VAR_NAME, default_location))
    set_cache_folder(str(folder))
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def clear_cache_folder():
    """
    Clear the cache.
    """
    cache_folder = get_cache_folder()
    rm_tree(cache_folder)


def list_cache_folder(max_levels=2):
    """
    List the cache.
    """
    cache_folder = get_cache_folder()
    print(ls_tree(cache_folder, max_levels=max_levels))
