import numpy as np
from pipetory import factory
import logging

# %%
X = np.random.uniform(0, 1, (10, 10))

# %%
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# %%
pipe = factory("sequential", "numpy", log)

# %%
@pipe.observe("square")
def square(x: np.ndarray) -> np.ndarray:
    return x ** 2

# %%
@pipe.observe("weighted_log", weight=0.5)
def weighted_log(x, weight):
    return weight * np.log(x)

# %%
pipe.compile()

# %%
res = pipe(X)

# %%
print(res)

