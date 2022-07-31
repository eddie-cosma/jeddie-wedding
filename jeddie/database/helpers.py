import random


def random_id():
    """Generate a random ID for party RSVP"""
    character_set = 'BCDFGHJKMPQRTVWXY2346789'
    return ''.join(random.choice(character_set) for i in range(6))
