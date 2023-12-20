#!/usr/bin/env python3
"""
Redis
"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps
UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator Counts how many times
    Methods of Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        This is wrapper function
        For call_calls method
        """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs
    For a particular function
    """
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """
        This is wrapper function
        For call_history method
        """
        self._redis.rpush(input_list, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output
    return wrapper


class Cache:
    """
    Class for methods that
    Operate a caching system
    """

    def __init__(self):
        """ Instance of Redis db """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self,
              data: UnionOfTypes) -> str:
        """
        Method takes a data argument and returns a string,
        Generate a random key (e.g. using uuid),
        Store the input data in Redis,
        using the random key and return the key
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves data stored at a key
        converts the data back to the desired format
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, data: str) -> str:
        """
        Get a string
        """
        return self.get(key, str)

    def get_int(self, data: str) -> int:
        """
        Get an int
        """
        return self.get(key, int)