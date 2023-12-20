#!/usr/bin/env python3
"""
This script changes all topics of a school document based on the name
"""

import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school
    Document based on name
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
