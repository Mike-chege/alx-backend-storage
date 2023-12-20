#!/usr/bin/env python3
"""
This script provides some stats
About Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


def print_stats(collection):
    # Total number of logs
    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    # Methods count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    # Count for specific method and path
    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client.logs
    collection = db.nginx

    # Print stats
    print_stats(collection)

    # Close MongoDB connection
    client.close()
