import string
import random
from typing import List, Set


def plane_id_generator(size=4, chars: List[str] = string.ascii_uppercase) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def get_planes_ids(count=10) -> Set[str]:
    ids : Set[str] = set()

    while len(ids) < count: # make sure there are no duplicates
        plane_id = plane_id_generator()
        if plane_id not in ids:
            ids.add(plane_id)

    return ids
