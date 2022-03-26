"""
The :mod:`pipetory.types.pipes` module contains the types associated with
pipelines.
"""

from enum import Enum, auto

class PipeTypes(Enum):
    """
    Enum for the different types of pipes.
    """
    SEQUENTIAL = auto()
    MERGER = auto()
    SPLITTER = auto()
