import sys
import time
from typing import TYPE_CHECKING

import usb.backend.libusb1  # type: ignore

import libusbfinder
import usb  # type: ignore

if TYPE_CHECKING:
    from usb.core import Device  # type: ignore

MAX_PACKET_SIZE = 0x4000


def acquire_device(timeout: float = 10) -> "Device":
    backend = usb.backend.libusb1.get_backend(
        find_library=lambda x: libusbfinder.libusb1_path()
    )

    start = time.time()
    # Keep retrying for up to timeout seconds if device is not found.
    while time.time() - start < timeout:
        device = usb.core.find(idVendor=0x5AC, idProduct=0x1281, backend=backend)
        if device is not None:
            return device
        sys.stdout.flush()
        time.sleep(0.1)
    print("ERROR: No Apple device in Recovery Mode 0x1281 detected. Exiting.")
    sys.exit(1)


def release_device(device: "Device") -> None:
    usb.util.dispose_resources(device)


def send_command(device: "Device", command: bytes) -> None:
    # TODO: Add assert?
    device.ctrl_transfer(0x40, 0, 0, 0, command + b"\x00", 30000)


def send_data(device: "Device", data: bytes) -> None:
    assert device.ctrl_transfer(0x41, 0, 0, 0, 0, 1000) == 0
    index = 0
    while index < len(data):
        amount = min(len(data) - index, MAX_PACKET_SIZE)
        assert device.write(0x04, data[index : index + amount], 1000) == amount
        index += amount
