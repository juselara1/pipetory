from pandas import DataFrame as PandasDf
from dask.dataframe import DataFrame as DaskDf
from modin.pandas import DataFrame as ModinDf
from ray.data import Dataset as RayDf
from typing import Sequence, Union, Callable, Optional, Any

PDataFrame = Union[PandasDf, DaskDf, ModinDf, RayDf]
MultiPDataFrame = Sequence[PDataFrame]
OptMultiPDataFrame = Union[PDataFrame, MultiPDataFrame]

Func = Callable[[OptMultiPDataFrame], OptMultiPDataFrame]
Args = Optional[Any]
Kwargs = Optional[Any]
Step = Optional[str]
