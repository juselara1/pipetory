from pipetory.types.pipes import PipeTypes
from pipetory.pipes.base import AbstractPipe
from pipetory.pipes.sequence import SequencePipe
from typing import Union
import logging

def factory(
        pipe_type: Union[PipeTypes, str],
        name: str,
        logger: logging.Logger = logging.getLogger()
        ) -> AbstractPipe:
    """
    Creates a pipe object based on the backend and type.

    Parameters
    ----------
    type : Union[PipeTypes, str]
        The type of pipe to create.

    Returns
    -------
    pipe : AbstractPipe
        The created pipe object.
    """
    if isinstance(pipe_type, str):
        pipe_type = PipeTypes[pipe_type.upper()]
    lut = {
            PipeTypes.SEQUENTIAL: SequencePipe(name, logger),
            PipeTypes.MERGER: SequencePipe(name, logger), # FIXME: Implement Merger Pipe
            PipeTypes.SPLITTER: SequencePipe(name, logger) # FIXME: Implement Splitter Pipe
            }
    
    return lut[pipe_type]

