from argparse import ArgumentParser

import h5py
from visr_reconstruction import visr_reconstruction
from typing import Optional
import fsspec
import logging

_log = logging.getLogger(__name__)


def _main(args: Optional[list[str]] = None) -> None:
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument(
        "--output-file",
        "-o",
        type=str,
        default="visr-reconstruction.png",
        help="Path to output PNG image file",
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input NEXUS file containing ViSR raw data",
    )
    parsed_args = parser.parse_args(args)
    input_file_path = parsed_args.input_file
    output_file_path = parsed_args.output_file
    _log.info(f"Loading {input_file_path}")
    with h5py.File(input_file_path, "r") as input_file:
        _log.info("Running ViSR reconstruction")
        reconstructed_data = visr_reconstruction(input_file)
        with fsspec.open(output_file_path, "wb") as output_file:
            _log.info(f"Writing output to: {output_file_path}")
            output_file.write(reconstructed_data.reconstructed_image)
    return


if __name__ == "__main__":
    _main()
