"""Backward-compatible import shim for the operational meaning scorer."""

from kaira.runtime.idl import InternalDeliberationLoop


class OperationalMeaningScorer:
    def score(self, *_args, **_kwargs) -> float:
        raise RuntimeError("Use RuntimeController or InternalDeliberationLoop for OMS computation in the new package layout.")


MeaningFunction = OperationalMeaningScorer

__all__ = ["OperationalMeaningScorer", "MeaningFunction", "InternalDeliberationLoop"]
