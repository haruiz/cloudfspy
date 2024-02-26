import logging

from dotenv import load_dotenv
from rich.logging import RichHandler

from .cloud_path import CloudPath, CloudPathFactory
from .generic_path import GenericPath
from .local_path import LocalPath
from .settings import *
from .vendors import *

load_dotenv()
FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False)],
)

__version__ = "0.1.0"
__name__ = "cloudfspy"
