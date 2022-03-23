from pipetory.types.exceptions import StepErrorKind

__step_err_msg = {
        StepErrorKind.VALUE_ERROR: "Step {} not found in {}.",
        StepErrorKind.LOCKED_ERROR: "Step {} from {} is locked.",
    }

class StepError(Exception):
    """
    StepError is raised when a step is not found in a pipeline.

    Attributes
    ----------
    kind : StepErrorKind
        The kind of error that occurred.
    step : str
        The name of the step.
    pipeline : str
        The name of the pipeline.
    """
    def __init__(self, kind: StepErrorKind, step: str, pipeline: str):
        self.kind = kind
        self.step = step
        self.pipeline = pipeline
        super().__init__(self.resolve())

    def resolve(self):
        return __step_err_msg[self.kind].format(self.step, self.pipeline)

    def __str__(self):
        return self.resolve()
