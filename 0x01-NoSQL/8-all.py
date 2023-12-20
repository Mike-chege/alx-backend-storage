#!/usr/bin/env python3
"""
This script lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    Returns a list of all documents
    In a collection or an empty list
    """
    return [each for each in mongo_collection.find()]
