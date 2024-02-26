import typing
from pathlib import Path

from .any_path import AnyPath
from .cloud_path import CloudPath
from .local_path import LocalPath
from .utils import is_valid_uri


class GenericPath(AnyPath):
    """
    Generic path class.
    """

    def __new__(cls, path: typing.Union[str, Path], *args, **kwargs):
        """
        Create a CloudPath object from a path.
        :param path: Path
        :param args: Arguments
        :param kwargs: Keyword arguments
        """
        # copy docs from Path class

        path = str(path)
        if is_valid_uri(path):
            return CloudPath(path, *args, **kwargs)
        else:
            return LocalPath(path, *args, **kwargs)
