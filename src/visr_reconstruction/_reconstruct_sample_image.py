from io import BytesIO
import h5py
from matplotlib.figure import Figure
from visr_reconstruction._input_data import VisrDataKey
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

_Array = NDArray[np.float64]


def reconstruct_sample_image(input_raw_data: h5py.Group) -> bytes:
    stage_positions = _load_stage_positions(input_raw_data)
    rgb_values = _load_raw_photo_sensor_rgb_values(input_raw_data)
    rgb_values = _normalize_rgb_values(rgb_values)
    figure = _plot_samples(stage_positions, rgb_values)
    return _convert_figure_to_png_bytes(figure)


def _load_raw_photo_sensor_rgb_values(input_raw_data: h5py.Group) -> _Array:
    red = np.ravel(input_raw_data[VisrDataKey.SPECTROSCOPY_DETECTOR_RED_TOTAL])
    green = np.ravel(input_raw_data[VisrDataKey.SPECTROSCOPY_DETECTOR_GREEN_TOTAL])
    blue = np.ravel(input_raw_data[VisrDataKey.SPECTROSCOPY_DETECTOR_BLUE_TOTAL])
    if not red.shape == green.shape == blue.shape:
        raise ValueError("invalid input data RBG array shapes don't match")
    rgb = np.vstack((red, green, blue), dtype=np.float64)
    assert rgb.shape == (3, red.shape[0])
    return rgb


def _load_stage_positions(input_raw_data: h5py.Group) -> _Array:
    stage_x = np.ravel(input_raw_data[VisrDataKey.STAGE_X])
    stage_y = np.ravel(input_raw_data[VisrDataKey.STAGE_Y])
    stage_positions = np.vstack((stage_x, stage_y), dtype=np.float64)
    if not stage_x.shape == stage_y.shape:
        raise ValueError("invalid input data stage positions don't match")
    assert stage_positions.shape == (2, stage_x.shape[0])
    return stage_positions


def _normalize_rgb_values(rgb_values: _Array) -> _Array:
    return rgb_values / float(np.max(rgb_values))


def _plot_samples(stage_positions: _Array, rgb_values: _Array) -> Figure:
    colors = np.mean(rgb_values, axis=0)
    figure = plt.figure(figsize=(6, 6))
    ax = figure.add_subplot(111)
    ax.scatter(
        stage_positions[0], stage_positions[1], c=colors, s=100, alpha=0.5, marker="s"
    )
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    return figure


def _convert_figure_to_png_bytes(figure: Figure) -> bytes:
    byte_buffer = BytesIO()
    figure.savefig(byte_buffer, format="png", bbox_inches="tight")
    byte_buffer.seek(0)
    return byte_buffer.getvalue()
