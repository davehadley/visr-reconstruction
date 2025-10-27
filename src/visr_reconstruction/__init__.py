import h5py
from dataclasses import dataclass
from ._reconstruct_sample_image import reconstruct_sample_image

__version__ = "0.1.0"


@dataclass(frozen=True)
class VisrReconstructionOutput:
    reconstructed_image: bytes


def visr_reconstruction(input_raw_data: h5py.Group) -> VisrReconstructionOutput:
    image_data = reconstruct_sample_image(input_raw_data)
    return VisrReconstructionOutput(image_data)
