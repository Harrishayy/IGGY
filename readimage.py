import numpy as np
import struct
import serial
from enum import Enum

class Format(Enum):
    RGB565 = 1
    GRAYSCALE = 2
    GRAYSCALE_INT = 3
def get_image(format, width, height, serial_handle=None, ser_data=None):
    """
    Retrieves image bytes from 'ser_data' if provided,
    else from 'serial_handle'.
    """
    pixels = width * height

    if format == Format.GRAYSCALE:
        bytes_per_pixel = 1
        data_type = np.uint8
        repres = 'B'
    elif format == Format.RGB565:
        bytes_per_pixel = 2
        data_type = np.uint16
        repres = 'H'
    else:
        bytes_per_pixel = 1
        data_type = np.uint8
        repres = 'b'

    bytes_to_read = pixels * bytes_per_pixel
    data_format = '>' + str(pixels) + repres

    # If the function is given 'ser_data', we use that. 
    # Otherwise, read from 'serial_handle' as a fallback.
    if ser_data is not None:
        data = ser_data
    else:
        data = serial_handle.read(bytes_to_read)

    raw_bytes = struct.unpack(data_format, data)

    if format == Format.RGB565:
        # Convert each 16-bit to R, G, B
        image = np.zeros((pixels, 3), dtype=np.uint8)
        for i, pixel in enumerate(raw_bytes):
            # RGB565 -> 24-bit
            r = ((pixel >> 11) & 0x1F) << 3
            g = ((pixel >> 5) & 0x3F) << 2
            b = (pixel & 0x1F) << 3
            image[i] = [r, g, b]
        return image.reshape((height, width, 3))

    # If it's grayscale, just reshape
    return np.array(raw_bytes, dtype=np.uint8).reshape((height, width))
