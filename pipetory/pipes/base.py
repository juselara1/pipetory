from abc import ABC, abstractmethod
from pipetory.types.dataset import OptMultiPDataFrame, Func, Kwargs, Step
from typing import Union, Dict, List
from functools import reduce, partial

def compose(f1: Func, f2: Func) -> Func:
    return lambda data: f1(f2(data))

class AbstractPipe(ABC):

    @abstractmethod
    def call(self, data: OptMultiPDataFrame, step: Step = None) -> OptMultiPDataFrame:
        ...

    @abstractmethod
    def register(self, func: Union[Func, "AbstractPipe"], step: Step, **kwargs: Kwargs) -> "AbstractPipe":
        ...

    @abstractmethod
    def compile(self) -> "AbstractPipe":
        ...

    @abstractmethod
    def repr(self) -> str:
        ...

class Pipe(AbstractPipe):
    def __init__(self, name: str):
        self.steps: List[str] = []
        self.funcs: Dict[str, Func] = {}
        self.cfuncs: Dict[str, Func] = {}
        self.name: str = name

    def __call__(self, data: OptMultiPDataFrame, step: Step = None) -> OptMultiPDataFrame:
        return self.call(data, step)

    def __repr__(self) -> str:
        return self.repr()
    
    def __str__(self) -> str:
        return self.repr()

    def compile(self) -> "Pipe":
        self.cfuncs = {}
        funcs = []
        for step in self.steps:
            func = self.funcs[step]
            if isinstance(func, Pipe):
                func = func.compile()
            funcs.append(self.funcs[step])
            self.cfuncs[step] = reduce(compose, funcs)
        return self

    def call(self, data: OptMultiPDataFrame, step: Step = None) -> OptMultiPDataFrame:
        valid_step = self.steps[-1] if step is None else step
        if valid_step not in self.steps:
            raise ValueError(f"Step {valid_step} not found in pipe: {self.name}")
        return self.cfuncs[valid_step](data)

    def register(self, func: Func, step: str, **kwargs: Kwargs) -> "Pipe":
        if kwargs is not None:
            func = partial(func, **kwargs)
        if step in self.funcs:
            print("[WARNING] Overwriting step {}".format(step))
        else:
            self.steps.append(step)
        self.funcs[step] = func
        return self
