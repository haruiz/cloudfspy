import logging

from rich.logging import RichHandler  # type: ignore

from .cloud_path import CloudPath
from .cloud_path import CloudPathFactory
from .generic_path import GenericPath
from .local_path import LocalPath
from .settings import clear_cache_folder
from .settings import get_cache_folder
from .settings import set_cache_folder
from .vendors import GCPCloudPath

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False)],
)

__version__ = "0.1.0"
__name__ = "cloudfspy"
