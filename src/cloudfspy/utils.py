import pathlib
import re
from urllib.parse import urlparse
import os
from colorama import Fore, Style

def get_uri_scheme(url) -> str or None:
    """
    Get the scheme from a URL.
    :param url:  URL
    :return: Scheme
    """
    pattern = r"^(.+?)://"
    match = re.match(pattern, url)
    if match:
        return match.group(1)  # Return the matched scheme
    return None


def is_valid_uri(uri: str) -> bool:
    """
    Check if a URI is valid.
    :param uri: URI
    :return: True if the URI is valid, False otherwise
    """
    try:
        result = urlparse(uri)
        # Check if the scheme and netloc are present
        return all([result.scheme, result.netloc])
    except:
        return False


def rm_tree(pth):
    """
    Remove a directory and its contents.
    :param pth:
    :return:
    """
    pth = pathlib.Path(pth)
    for child in pth.glob("*"):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


import os

def ls_tree(startpath, max_levels, symbol="-", indent=0):
    if max_levels < 0:  # Base case to stop recursion
        return ''
    
    output = ''
    # Use the provided symbol as the indicator for each level
    prefix = '    ' * indent + (symbol + ' ' if indent > 0 else '')
    output += prefix + os.path.basename(startpath) + '\n'
    prefix = '    ' * (indent + 1) + symbol + ' '
    
    if indent >= max_levels:  # Stop diving into directories if max depth is reached
        return output
    
    try:
        for item in os.listdir(startpath):
            path = os.path.join(startpath, item)
            if os.path.isdir(path):
                output += ls_tree(path, max_levels - 1, symbol, indent + 1)
            else:
                output += prefix + item + '\n'
    except PermissionError:
        output += prefix + 'Permission denied' + '\n'
    
    return output

