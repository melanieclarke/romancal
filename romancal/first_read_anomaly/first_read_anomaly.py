import numpy as np
from roman_datamodels import dqflags

__all__ = ["mask_affected_rows", "correct_anomaly"]


def mask_affected_rows(groupdq):
    """
    Mask all rows likely to be affected by the transient anomaly.

    Parameters
    ----------
    groupdq : `~numpy.ndarray`
        The group DQ image.  Updated in place.
    """
    groupdq[0, :1000, :] |= dqflags.group.DO_NOT_USE


def correct_anomaly(input_model, mask_rows=False):
    """
    Correct the transient first read anomaly.

    Parameters
    ----------
    input_model : `~roman_datamodels.datamodels.`
    mask_rows

    Returns
    -------

    """
    # Fallback option: just mask the affected rows in the first read
    if mask_rows:
        mask_affected_rows(input_model.groupdq)
        return input_model

    return input_model
