import random
import string
from typing import List, Set


def generate_plane_id(size: int = 4, chars: List[str] = string.ascii_uppercase) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def generate_plane_ids(count: int = 10) -> Set[str]:
    ids: Set[str] = set()

    while len(ids) < count:  # make sure there are no duplicates
        plane_id = generate_plane_id()
        if plane_id not in ids:
            ids.add(plane_id)

    return ids
