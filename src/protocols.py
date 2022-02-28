try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class Object(Protocol):
    def to_dict(self) -> dict:
        ...
