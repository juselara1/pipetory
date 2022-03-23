from typing import Protocol, Union, Sequence, Any, Optional, List

class DataArray(Protocol):
    """
    The DataArray protocol defines the methods that a data array should implement.
    """
    def __getitem__(
            self,
            key: Union[int, slice]
            ) -> Union[Any, List[Any]]:
        """
        Returns the item at the given index or slice.

        Parameters
        ----------
        key : int or slice
            The index or slice to get.

        Returns
        -------
        Any
            The item or items at the given index or slice.
        """
        ...

    def __len__(self) -> int:
        """
        Returns the length of the data array.

        Returns
        -------
        int
            The length of the data array.
        """
        ...

    def __iter__(self) -> Any:
        """
        Returns an iterator over the data array.
        
        Returns
        -------
        Any
            An iterator over the data array.
        """
        ...

MultiArray = Sequence[DataArray]
DataSet = Union[DataArray, MultiArray]
OptDataSet = Optional[DataSet]
