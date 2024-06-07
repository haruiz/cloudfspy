import os
import typing
from pathlib import _posix_flavour  # type: ignore
from pathlib import _windows_flavour  # type: ignore
from pathlib import Path as _Path_

if typing.TYPE_CHECKING:
    from . import GenericPath
    from .local_path import LocalPath
    from .cloud_path import CloudPath


class AnyPath(_Path_):
    """
    GenericPath class is an abstract class
    """

    _flavour = _windows_flavour if os.name == "nt" else _posix_flavour

    def upload_to(
        self,
        destination: typing.Union[str, "GenericPath", "CloudPath"],
        *args,
        **kwargs,
    ) -> "CloudPath":
        """
        Upload a file to a destination.
        :param destination: Destination path
        """
        raise NotImplementedError

    def download_to(
        self,
        destination: typing.Union[str, "GenericPath", "LocalPath"],
        *args,
        **kwargs,
    ) -> "LocalPath":
        """
        Download a file to a destination.
        :param destination: Destination path
        """
        raise NotImplementedError
