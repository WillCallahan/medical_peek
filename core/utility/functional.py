import logging
from functools import reduce
from typing import Callable, Optional, List

logger = logging.getLogger(__name__)


def thread_first(*funcs_and_args):
    """
    Threads a parameter to each tuple

    Example:
        thread_first(
            [1, 2, 3],
            (sum,),
            (lambda x: max(x, 4)),
        )
        # max(sum([1, 2, 3]), 4)
        # Returns 6

    :param funcs_and_args: Tuples of functions and function parameters
    :type funcs_and_args: *
    :return: Threaded return variable
    :rtype: *
    """
    return reduce(lambda x, y: y[0](*(y[1:] + (x,))), funcs_and_args)


def thread_last(*funcs_and_args):
    """
    Threads a parameter to each tuple in reverse order

    Example:
        thread_last(
            [1, 2, 3],
            (sum,),
            (lambda x: max(*x, 4)),
        )
        # sum(max([1, 2, 3], 4))
        # Returns 4

    :param funcs_and_args: Threaded return variable
    :type funcs_and_args: *
    :return: Threaded return variable
    :rtype: *
    """
    return thread_first((funcs_and_args[0],) + tuple(reversed(funcs_and_args[1:])))


def return_argument(n, *args):
    """
    Returns the argument at the specified index

    :param n: Index to return
    :type n: int
    :param args: Arguments to search through
    :type args: *
    :return: Argument at index n
    :rtype: *
    """
    return args[n]


def debug(x):
    """
    Debugs a threaded variable

    :param x: Variable to debug
    :type x: *
    :return: Variable passed in
    :rtype: *
    """
    logger.log(logging.DEBUG, x)
    return x


def log(level, message, x):
    """
    Debugs a message and returns the last variable

    :param level: Variable to debug
    :type level: *
    :param message: Variable to debug
    :type message: *
    :param x: Variable to thread through
    :type x: *
    :return: Variable passed in
    :rtype: *
    """
    logger.log(level, message)
    return x


def log_length(level, message, x):
    """
    Debugs a message and returns the last variable

    :param level: Variable to debug
    :type level: str
    :param message: Variable to debug
    :type message: str
    :param x: Variable to thread through
    :type x: *
    :return: Variable passed in
    :rtype: *
    """
    items = list(x)
    logger.log(level, message.format(len(items)))
    return items


def is_not(func):
    """
    Returns the inverse of the return value of the provided function

    :param func: Function to invert
    :type func: *
    :return: Inverted return value function
    :rtype: *
    """
    return lambda *args, **kwargs: not func(*args, **kwargs)


def group_by(iterable: iter, key_func: Callable, val_func: Optional[Callable] = None):
    """
    Groups objects together

    :param iterable: Iterable to group
    :type iterable: iter
    :param key_func: Key Function to group values
    :type key_func: Callable
    :param val_func: Value Function to get value from object
    :type val_func: Optional[Callable]
    :return: Grouped Objects
    :rtype: dict
    """
    vals = {}
    val_func = val_func or (lambda x: x)
    for obj in iterable:
        key = key_func(obj)
        value = val_func(obj)
        vals.setdefault(key, []).append(value)
    return vals


def dict_to_kvp(dictionary: dict) -> List[tuple]:
    """
    Converts a dictionary to a list of tuples where each tuple has the key and value
    of each dictionary item

    :param dictionary: Dictionary to convert
    :return: List of Key-Value Pairs
    """
    return [(k, v) for k, v in dictionary.items()]


def to_dictionary(iterable: iter, key_func, val_func: Optional[Callable] = None):
    """
    Converts an iterable to a dictionary

    :param iterable: Iterable to convert
    :type iterable: iter
    :param key_func: Key Function of the each object
    :type key_func: Callable
    :param val_func: Value Function to get values
    :type val_func: Optional[Callable]
    :return: Dictionary
    :rtype: dict
    """
    val_func = val_func or (lambda x: x)
    return {key_func(obj): val_func(obj) for obj in iterable}


def concat(list_a: list, list_b: list) -> list:
    """
    Concatenates two lists together into a new list

    Example:
       >>> concat([1, 2, 3], [4, 5, 6])
       ... [1, 2, 3, 4, 5 6]


    :param list_a: First list to concatenate
    :param list_b: Second list to concatenate
    :return: Concatenated list
    """
    result = list_a + list_b
    return result


def join(separator, iterable: list) -> str:
    """
    Joins an iterable of objects together with a separator in between

    :param separator: Separator to use in between joined strings
    :param iterable: Iterable of objects to convert to a joined string
    :return: Joined String
    """
    return str(separator).join(list(map(str, iterable)))


def log_message(log_level, message, x):
    """
    Logs a message

    :param log_level: Variable to debug
    :type log_level: int
    :param message: Message to log
    :type message: str
    :param x: Variable to debug
    :type x: *
    :return: Variable passed in
    :rtype: *
    """
    logger.log(log_level, message)
    return x


def select_keys(keys: list, m: dict):
    """
    Selects specific keys in a map
    :param keys: Keys to select
    :param m: map to filter
    :return: map
    """
    new_map = {}
    for key, value in m.items():
        if key in keys:
            new_map[key] = value
    return new_map


def flatten(arr: List[List]) -> List:
    """
    Flattens a list of a list
    :param arr: List to flatten
    :return: Flattened list
    """
    return reduce(lambda x, y: x + y, arr)


def rename_keys(iterable: dict, key_func: Callable):
    """
    Renames the keys in a dictionary
    :param iterable: Dictionary to iterate through
    :param key_func: Function to generate the new key name
    :return: Dictionary with new key names
    """
    return {key_func(k): v for k, v in iterable.items()}


def single(match_func: callable, iterable):
    """
    Gets the first instance of a match provided with the true response of the match_func
    :param match_func: Function called for each element in the iterable
    :param iterable: Iterable to iterate through
    :return: First matching element or None if there is no match
    """
    if not iterable:
        return None
    for element in iterable:
        is_match = match_func(element)
        if is_match:
            return element
    return None


def first(iterable):
    """
    Gets the first element from an iterable. If there are no items or there
    are not enough items, then None will be returned.
    :param iterable: Iterable
    :return: First element from the iterable
    """
    if iterable is None or len(iterable) == 0:
        return None
    return iterable[0]


def second(iterable):
    """
    Gets the second element from an iterable. If there are no items are not
    enough items, then None will be returned.
    :param iterable: Iterable
    :return: Second element from the iterable
    """
    if iterable is None or len(iterable) < 1:
        return None
    return iterable[1]


def keys(iterable):
    """
    Gets the keys from a dictionary or the first item of an iterable of iterables
    :param iterable: Iterable to get keys from
    :return: Keys from the iterable
    """
    if iterable is None:
        return []
    if isinstance(iterable, dict):
        return iterable.keys()
    return [first(o) for o in iterable]
