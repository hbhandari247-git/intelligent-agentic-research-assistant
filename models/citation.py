from dataclasses import dataclass


@dataclass(slots=True)
class Citation:
    title: str
    location: str
    url: str | None = None
