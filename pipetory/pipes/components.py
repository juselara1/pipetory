from pipetory.pipes.base import Pipe

class Sequencer(Pipe):
    """
    Sequencer is a Pipe that sequentially executes the given pipes.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def repr(self):
        return(f"Sequencer(name={self.name})")

class Merger(Pipe):
    """
    Merger is a Pipe that merges the given pipes.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def repr(self):
        return(f"Merger(name={self.name})")

class Splitter(Pipe):
    """
    Splitter is a Pipe that splits the given pipes.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def repr(self):
        return(f"Splitter(name={self.name})")
