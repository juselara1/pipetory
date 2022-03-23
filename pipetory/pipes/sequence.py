from pipetory.pipes.base import AbstractSequencer
from pipetory.types.data import DataArray
from pipetory.types.functions import Step, Kwargs
from pipetory.types.exceptions import StepErrorKind
from pipetory.exceptions.steps import StepError
from pipetory.futils.combine import compose
from typing import List, Dict, Callable
from functools import partial, reduce
import logging

SFunc = Callable[[DataArray], DataArray]

class SequencePipe(AbstractSequencer):
    """
    A pipe that sequentially executes the given pipes.

    Attributes
    ----------
    name : str
        The name of the pipe.
    """
    def __init__(self, name: str, logger=logging.getLogger()):
        self.name = name
        self.logger = logger
        self.steps: List[str] = []
        self.locked: Dict[str, bool] = {}
        self.funcs: Dict[str, SFunc] = {}
        self.cfuncs: Dict[str, SFunc] = {}
        self.last_step: str = ""

    def call(self, data: DataArray, step: Step) -> DataArray:
        """
        Executes the pipe.

        Parameters
        ----------
        data : DataArray
            The data to be passed to the pipe.
        step : Step
            The step to be executed.

        Returns
        -------
        DataArray
            The result of the pipe.
        """
        selected_step = self.last_step if step is None else step
        if selected_step not in self.funcs:
            raise StepError(
                    kind=StepErrorKind.VALUE_ERROR,
                    step=selected_step,
                    pipeline=self.name
                    )
        elif self.is_locked(selected_step):
            raise StepError(
                    kind=StepErrorKind.LOCKED_ERROR,
                    step=selected_step,
                    pipeline=self.name
                    )
        else:
            return self.cfuncs[selected_step](data)

    def register(self, func: Callable, step: str, **kwargs: Kwargs) -> "SequencePipe":
        """
        Registers a function to be executed in the pipe.

        Parameters
        ----------
        func : Callable
            The function to be executed.
        step: str
            The name of the step.
        kwargs : Kwargs
            The keyword arguments to be passed to the function.
        """
        self.logger.info(f"Registering step {step} in {self.name}")
        if kwargs is not None:
            func = partial(func, **kwargs)
        if step in self.funcs:
            self.logger.warning(f"Overwriting step {step} in {self.name}")
        else:
            self.steps.append(step)
            self.last_step = step
        self.funcs[step] = func
        self.locked[step] = False
        return self

    def observe(self, step: str, **kwargs: Kwargs):
        """
        Creates a decorator that tracks a step.

        Parameters
        ----------
        step : str
            The name of the step.
        kwargs : Kwargs
            The keyword arguments to be passed to the function.

        Returns
        -------
        Callable
            The decorator.
        """
        def decorator(func: Callable) -> SFunc:
            self.register(func, step, **kwargs)
            return self.funcs[step]
        return decorator

    def log_step(self, func: SFunc, step: str) -> SFunc:
        """
        Logs the execution of a step.

        Parameters
        ----------
        func : SFunc
            The function to be logged.
        step : str
            The name of the step.

        Returns
        -------
        SFunc
            The logged function.
        """
        def wrapper(data: DataArray) -> DataArray:
            self.logger.info(f"Executing step {step} in {self.name}")
            return func(data)
        return wrapper

    def compile(self) -> "SequencePipe":
        """
        Compiles the pipe.

        Returns
        -------
        SequencePipe
            The compiled pipe.
        """

        self.cfuncs = {}
        funcs = []
        for step in self.steps:
            if self.is_locked(step):
                continue
            logged_func = self.log_step(self.funcs[step], step)
            funcs.append(logged_func)
            self.cfuncs[step] = reduce(compose, funcs)
        return self

    def repr(self) -> str:
        return f"Sequencer(name={self.name}, n_steps={self.n_steps})"
