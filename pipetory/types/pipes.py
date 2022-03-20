from enum import Enum

class PipeTypes(Enum):
    """
    Enum for the different types of pipes.
    """
    SEQUENTIAL = 1
    MERGER = 2
    SPLITTER = 3
