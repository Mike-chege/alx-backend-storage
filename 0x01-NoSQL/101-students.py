#!/usr/bin/env python3
"""
This script returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Returns all students sorted
    By average score
    """
    return list(mongo_collection.find())
