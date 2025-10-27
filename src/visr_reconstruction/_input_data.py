import enum


class VisrDataKey(enum.StrEnum):
    SPECTROSCOPY_DETECTOR_RED_TOTAL = (
        "entry/instrument/spectroscopy_detector/RedTotal",
    )
    SPECTROSCOPY_DETECTOR_GREEN_TOTAL = (
        "entry/instrument/spectroscopy_detector/GreenTotal"
    )
    SPECTROSCOPY_DETECTOR_BLUE_TOTAL = (
        "entry/instrument/spectroscopy_detector/BlueTotal"
    )
    STAGE_X = "entry/instrument/sample_stage/x"
    STAGE_Y = "entry/instrument/sample_stage/y"
