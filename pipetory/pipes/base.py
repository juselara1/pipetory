from abc import ABC, abstractmethod
from pipetory.types.functions import Args, Kwargs, Step
from pipetory.types.data import DataArray, MultiArray, DataSet
from typing import Union, Dict, List, Callable

GFunc = Callable[[DataSet], DataSet]

class Lockable:
    """
    Lockable is a mixin class that provides a lock mechanism for steps.

    Attributes
    ----------
    locked: Dict[str, bool]
        A dictionary of steps and their locked status.
    """
    locked: Dict[str, bool]

    def is_locked(self, step: str) -> bool:
        """
        Returns whether a step is locked.

        Parameters
        ----------
        step: str
            The step to check.

        Returns
        -------
        bool
            Whether the step is locked.
        """
        return self.locked[step]

    def lock(self, step: str):
        """
        Locks a step.

        Parameters
        ----------
        step: str
            The step to lock.
        """
        self.locked[step] = True

    def unlock(self, step: str):
        """
        Unlocks a step.

        Parameters
        ----------
        step: str
            The step to unlock.
        """
        self.locked[step] = False

    def lock_all(self):
        """
        Locks all steps.
        """
        for step in self.locked:
            self.lock(step)

    def unlock_all(self):
        """
        Unlocks all steps.
        """
        for step in self.locked:
            self.unlock(step)

class AbstractPipe(ABC, Lockable):
    """
    AbstractPipe is an abstract class that provides a pipeline interface.

    Attributes
    ----------
    steps: List[str]
        A list of steps in the pipeline.
    """
    steps: List[str]

    @abstractmethod
    def call(self, data: DataSet, step: Step = None) -> DataSet:
        """
        The call step implements the pipeline interface.

        Parameters
        ----------
        data: DataSet
            The data to process.
        step: Step
            The step to process.

        Returns
        -------
        DataSet
            The processed data.
        """
        ...

    @abstractmethod
    def register(
            self,
            func: Union[GFunc, "AbstractPipe"],
            step: Step,
            *args: Args,
            **kwargs: Kwargs
            ) -> "AbstractPipe":
        """
        Registers a function in a given step.

        Parameters
        ----------
        func: Union[GFunc, AbstractPipe]
            The function to register.
        step: Step
            The step to register the function to.
        args: Args
            The arguments to pass to the function.
        kwargs: Kwargs
            The keyword arguments to pass to the function.
        """
        ...

    @abstractmethod
    def observe(
            self, step: str,
            *args: Args,
            **kwargs: Kwargs
            ) -> Callable[[Callable], GFunc]:
        """
        Decorates a function to be registered in a given step.

        Parameters
        ----------
        step: str
            The step to register the function to.
        args: Args
            The arguments to pass to the function.
        kwargs: Kwargs
            The keyword arguments to pass to the function.
        """
        ...

    @abstractmethod
    def compile(self) -> "AbstractPipe":
        """
        Compiles the pipeline.

        Returns
        -------
        AbstractPipe
            The compiled pipeline.
        """
        ...

    @abstractmethod
    def repr(self) -> str:
        """
        Returns a string representation of the pipeline.

        Returns
        -------
        str
            The string representation of the pipeline.
        """
        ...

    @abstractmethod
    def log_step(
            self,
            func: Union[GFunc, "AbstractPipe"],
            step: str
            ) -> Union[GFunc, "AbstractPipe"]:
        """
        Adds logging to a function.

        Parameters
        ----------
        func: Union[GFunc, AbstractPipe]
            The function to log.
        step: str
            The step to log the function to.

        Returns
        -------
        Union[GFunc, AbstractPipe]
            The logged function.
        """
        ...

    @property
    def n_steps(self) -> int:
        """
        Returns the number of steps in the pipeline.

        Returns
        -------
        int
            The number of steps in the pipeline.
        """
        return len(self.steps)

    def __repr__(self) -> str:
        """
        Returns a string representation of the pipeline.

        Returns
        -------
        str
            The string representation of the pipeline.
        """
        return self.repr()

    def __str__(self) -> str:
        """
        Returns a string representation of the pipeline.
        
        Returns
        -------
        str
            The string representation of the pipeline.
        """
        return self.repr()

    def __call__(self, data: DataSet, step: Step = None) -> DataSet:
        """
        The call step implements the pipeline interface.

        Parameters
        ----------
        data: DataSet
            The data to process.
        step: Step
            The step to process.

        Returns
        -------
        DataSet
            The processed data.
        """
        return self.call(data, step)

class AbstractSequencer(AbstractPipe):
    """
    AbstractSequencer is an abstract class with a sequence call.
    """
    @abstractmethod
    def call(self, data: DataArray, step: Step = None) -> DataArray:
        """
        The call method implements a composed function.

        Parameters
        ----------
        data: DataArray
            The data to process.
        step: Step
            The step to process.

        Returns
        -------
        DataArray
            The processed data.
        """

        ...

class AbstractParalleler(AbstractPipe):
    """
    AbstractParalleler is an abstract class with a parallel call.
    """

    @abstractmethod
    def call(self, data: MultiArray, step: Step = None) -> MultiArray:
        """
        The call method implements a parallel set of independent functions.

        Parameters
        ----------
        data: MultiArray
            The data to process.
        step: Step
            The step to process.

        Returns
        -------
        MultiArray
            The processed data.
        """
        ...

class AbstractMerger(AbstractPipe):
    """
    AbstractMerger is an abstract class with a merge call.
    """
    
    @abstractmethod
    def call(self, data: MultiArray, step: Step = None) -> DataArray:
        """
        The call method implements a composed function that merges multiple inputs into a single one.

        Parameters
        ----------
        data: MultiArray
            The data to process.
        step: Step
            The step to process.

        Returns
        -------
        DataArray
            The processed data.
        """
        ...

class AbstractSplitter(AbstractPipe):
    """
    AbstractSplitter is an abstract class with a split call.
    """

    @abstractmethod
    def call(self, data: DataArray, step: Step = None) -> MultiArray:
        """
        The call method implements a composed function that splits a single input into multiple outputs.

        Parameters
        ----------
        data: DataArray
            The data to process.
        step: Step
            The step to process.

        Returns
        -------
        MultiArray
            The processed data.
        """
        ...
