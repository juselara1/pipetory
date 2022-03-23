from enum import Enum, auto

class StepErrorKind(Enum):
    """
    Enum for the different kinds of errors that can occur during the execution of a step.
    """
    VALUE_ERROR = auto()
    LOCKED_ERROR = auto()
