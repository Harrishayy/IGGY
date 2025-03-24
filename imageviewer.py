import serial
import time
import readimage
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime

# Camera dimensions
WIDTH = 176
HEIGHT = 144

# Open the serial port at the same baud rate as Arduino
ser = serial.Serial('/dev/cu.usbmodem101', baudrate=9600, timeout=2)

while True:
    # Send a command to tell Arduino to capture one frame
    ser.write(b'capture\n')
    # Give Arduino a moment to capture and send
    time.sleep(2)

    # We expect 176 * 144 * 2 bytes for RGB565
    bytes_to_read = WIDTH * HEIGHT * 2

    # Read raw bytes
    data = ser.read(bytes_to_read)
    if len(data) != bytes_to_read:
        print(f"Error: expected {bytes_to_read} bytes, got {len(data)}")
        # You might decide to break or continue here
        continue

    # Decode using your readimage.py logic (Format.RGB565)
    image_np = readimage.get_image(readimage.Format.RGB565, WIDTH, HEIGHT, ser_data=data)

    # Show the image
    # Note: For RGB, we typically do: plt.imshow(image_np) after converting to [0..1] or [0..255]
    # But the helper returns array shaped (HEIGHT, WIDTH, 3) in 8-bit, so we can just show directly:
    plt.imshow(image_np)
    plt.axis('off') 
    plt.show()

    # Optionally save
    save_prompt = input("Save image? (y/n) ")
    if save_prompt.lower() == 'y':
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"ard_{timestamp}.jpg"
        cv2.imwrite(filename, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
        print(f"Saved {filename}")
