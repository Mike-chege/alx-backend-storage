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
    """Decorator Counts how many times methods of Cache class are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """This is a wrapper function for count_calls method"""
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """This is a wrapper function for call_history method"""
        str_args = [str(arg) for arg in args]  # Convert args to strings
        self._redis.rpush(input_list, str(str_args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output
    return wrapper

class Cache:
    """Class for methods that operate a caching system"""

    # ... (other code)

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Method takes a data argument and returns a string
        Generate a random key (e.g. using uuid), store the input data in Redis
        using the random key and return the key
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    # ... (other code)

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves data stored at a key
        Converts the data back to the desired format
        """
        data = self._redis.get(key)
        return fn(data) if (fn and data is not None) else data

    def get_str(self, key: str) -> str:
        """Get a string"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Get an int"""
        return self.get(key, int)
