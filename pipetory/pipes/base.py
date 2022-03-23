from abc import ABC, abstractmethod
from pipetory.types.functions import Kwargs, Step
from pipetory.types.data import DataArray, MultiArray, DataSet
from typing import Union, Dict, List, Callable
from functools import reduce, partial

GFunc = Callable[[DataSet], DataSet]

class AbstractPipe(ABC):
    steps: List[str]

    @abstractmethod
    def call(self, data: DataSet, step: Step = None) -> DataSet:
        ...

    @abstractmethod
    def register(self, func: Union[GFunc, "AbstractPipe"], step: Step, **kwargs: Kwargs) -> "AbstractPipe":
        ...

    @abstractmethod
    def observe(self, step: str, kwargs: Kwargs) -> GFunc:
        ...

    @abstractmethod
    def compile(self) -> "AbstractPipe":
        ...

    @abstractmethod
    def repr(self) -> str:
        ...

    @abstractmethod
    def log_step(
            self,
            func: Union[GFunc, "AbstractPipe"],
            step: str
            ) -> Union[GFunc, "AbstractPipe"]:
        ...

    @property
    def n_steps(self) -> int:
        return len(self.steps)

    def __repr__(self) -> str:
        return self.repr()

    def __str__(self) -> str:
        return self.repr()

    def __call__(self, data: DataSet, step: Step = None) -> DataSet:
        return self.call(data, step)

class Lockable:
    locked: Dict[str, bool]

    def is_locked(self, step: str) -> bool:
        return self.locked[step]

    def lock(self, step: str):
        self.locked[step] = True

    def unlock(self, step: str):
        self.locked[step] = False

    def lock_all(self):
        for step in self.locked:
            self.lock(step)

    def unlock_all(self):
        for step in self.locked:
            self.unlock(step)

class AbstractSequencer(AbstractPipe, Lockable):
    
    @abstractmethod
    def call(self, data: DataArray, step: Step = None) -> DataArray:
        ...

class AbstractParalleler(AbstractPipe, Lockable):

    @abstractmethod
    def call(self, data: MultiArray, step: Step = None) -> MultiArray:
        ...

class AbstractMerger(AbstractPipe, Lockable):
    
    @abstractmethod
    def call(self, data: MultiArray, step: Step = None) -> DataArray:
        ...

class AbstractSplitter(AbstractPipe, Lockable):
    
    @abstractmethod
    def call(self, data: DataArray, step: Step = None) -> MultiArray:
        ...
