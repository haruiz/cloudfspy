import logging
import sys
import traceback
from functools import wraps

log = logging.getLogger("rich")


def exception(function):
    """
    Decorator to log exceptions.
    :param function: function to decorate.
    :return: decorated function.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        """
        Wrapper function to log exceptions.
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return function(*args, **kwargs)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc_message = traceback.format_exception_only(exc_type, exc_value)[0]
            log.exception(
                " Calling the function `{}` -> {} ".format(
                    function.__qualname__, exc_message
                )
            )
            raise

    return wrapper


def gcp_exception(function):
    """
    Decorator to log exceptions.
    :param function: function to decorate.
    :return:
    """
    try:
        from google.cloud.exceptions import NotFound, BadRequest, Forbidden  # type: ignore
    except ImportError:
        raise ImportError(
            "Please install google-cloud-storage using pip install google-cloud-storage"
        )

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to catch exceptions.
        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return function(self, *args, **kwargs)
        except (NotFound, BadRequest, Forbidden, Exception) as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc_message = traceback.format_exception_only(exc_type, exc_value)[0]

            error_messages = {
                NotFound: "bucket not found",
                BadRequest: "Invalid request to the gcp file",
                Forbidden: "Access to the gcp path is forbidden",
            }
            log.exception(
                f"Calling the function `{function.__qualname__}` "
                f"-> {error_messages.get(type(ex), 'Unknown error')} : {exc_message}"
            )
            raise

    return wrapper
