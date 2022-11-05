from typing import List
from dataclasses import dataclass

@dataclass
class MusicInfo:
    title: str
    authors: List[str]