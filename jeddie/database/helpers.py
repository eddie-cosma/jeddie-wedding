"""
Database helper functions.

This module provides utility functions for database operations.
"""

import uuid


def generate_uuid():
    """
    Generate a random UUID for party RSVP identification.
    
    This function is used to create unique identifiers for parties in the RSVP system.
    The UUIDs are used in URLs and provide a secure way to identify parties without
    exposing internal database IDs.
    
    Returns:
        str: A random UUID v4 string
    """
    return str(uuid.uuid4())
