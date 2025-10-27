from io import BytesIO
import h5py
import numpy as np
from visr_reconstruction._input_data import VisrDataKey
from visr_reconstruction import visr_reconstruction
from PIL import Image


def _mock_h5py_data() -> h5py.Group:
    rand = np.random.RandomState(1234)
    mock_data = h5py.File.in_memory()
    shape = (900,)
    for key in VisrDataKey:
        mock_data[key] = rand.uniform(size=shape)
    return mock_data


def test_visr_reconstruction_produces_valid_image() -> None:
    data = _mock_h5py_data()
    output = visr_reconstruction(data)
    png_bytes = output.reconstructed_image
    with Image.open(BytesIO(png_bytes)) as img:
        img.verify()
    with Image.open(BytesIO(png_bytes)) as img:
        img.load()
    assert img.format == "PNG"
    assert img.size[0] > 0 and img.size[1] > 0
