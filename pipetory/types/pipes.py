from enum import Enum, auto

class PipeTypes(Enum):
    """
    Enum for the different types of pipes.
    """
    SEQUENTIAL = auto()
    MERGER = auto()
    SPLITTER = auto()
