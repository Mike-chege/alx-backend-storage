#!/usr/bin/env python3
"""
This script returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school
    Having a specific topic
    """
    return mongo_collection.find({"topics": topic})
