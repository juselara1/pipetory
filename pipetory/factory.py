from pipetory.types.pipes import PipeTypes
from pipetory.pipes.base import Pipe
from pipetory.pipes.components import Sequencer, Merger, Splitter
from typing import Union

def factory(pipe_type: Union[PipeTypes, str], name: str) -> Pipe:
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
            PipeTypes.SEQUENTIAL: Sequencer(name),
            PipeTypes.MERGER: Merger(name),
            PipeTypes.SPLITTER: Splitter(name)
            }
    
    return lut[pipe_type]

