#! /usr/bin/env python
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import roman_datamodels as rdm

from romancal.first_read_anomaly.first_read_anomaly import correct_anomaly
from romancal.stpipe import RomanStep

if TYPE_CHECKING:
    from typing import ClassVar

__all__ = ["FirstReadAnomalyStep"]

log = logging.getLogger(__name__)


class FirstReadAnomalyStep(RomanStep):
    """
    Correct a transient anomaly in the first read.

    This correction applies to detector WFI18 only.
    """

    class_alias = "first_read_anomaly"
    reference_file_types: ClassVar = []

    spec = """
        mask_rows = boolean(default = False) # Just mask the affected rows
    """


    def process(self, input_data):
        if isinstance(input_data, rdm.DataModel):
            input_model = input_data
        else:
            # Open the input data model
            input_model = rdm.open(input_data)

        if input_model.meta.instrument.detector != "WFI18":
            log.warning("First read anomaly correction is implemented only for WFI18")
            input_model.meta.cal_step.first_read_anomaly = "SKIPPED"
            return input_model

        log.info("Correcting the first read anomaly for WFI18")
        output_model = correct_anomaly(input_model, mask_rows=self.mask_rows)
        output_model.meta.cal_step.first_read_anomaly = "COMPLETE"

        if self.save_results:
            try:
                self.suffix = "first_read_anomaly"
            except AttributeError:
                self["suffix"] = "first_read_anomaly"

        return output_model
