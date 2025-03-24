import serial
import serial.tools.list_ports
import numpy as np
import cv2
import time

def list_ports():
    """
    List available serial ports.
    """
    ports = list(serial.tools.list_ports.comports())
    print("Available serial ports:")
    for p in ports:
        print("  -", p.device)
    return ports

def read_full_frame(ser, frame_size, timeout=5):
    """
    Continuously reads available bytes from the serial port and accumulates them until 
    a complete frame (of size frame_size) is obtained or timeout is reached.
    """
    buffer = bytearray()
    start_time = time.time()
    while len(buffer) < frame_size:
        if ser.in_waiting > 0:
            new_bytes = ser.read(ser.in_waiting)
            buffer.extend(new_bytes)
        if time.time() - start_time > timeout:
            print(f"Timeout: only {len(buffer)} bytes received, expected {frame_size} bytes.")
            return None
        time.sleep(0.005)
    return bytes(buffer)

def convert_rgb565_to_rgb(frame_buffer, camera_width, camera_height):
    """
    Converts a byte buffer of RGB565 data to an RGB image (NumPy array).
    """
    # Try little-endian format; if that doesn't work, try switching to big-endian.
    pixels = np.frombuffer(frame_buffer, dtype='<u2')
    print("First 20 raw pixel values (little-endian):", pixels[:20])
    print("Unique pixel values (little-endian):", np.unique(pixels))
    
    # Extract channels from RGB565: 5 bits for red, 6 bits for green, 5 bits for blue
    r = ((pixels >> 11) & 0x1F) << 3
    g = ((pixels >> 5) & 0x3F) << 2
    b = (pixels & 0x1F) << 3
    
    # Combine channels and reshape into the image dimensions
    img = np.stack([r, g, b], axis=-1).reshape((camera_height, camera_width, 3))
    return img

def main():
    # Camera parameters: must match your Arduino sketch (QCIF: 176x144, RGB565)
    camera_width = 176
    camera_height = 144
    camera_bytes_per_pixel = 2
    bytes_per_frame = camera_width * camera_height * camera_bytes_per_pixel  # Expected: 50688

    list_ports()

    port_name = '/dev/cu.usbmodem1101'  # Adjust as needed (e.g., COM3 on Windows)
    baud_rate = 115200

    try:
        ser = serial.Serial(port_name, baud_rate, timeout=2)
    except Exception as e:
        print("Failed to open serial port:", e)
        return

    time.sleep(2)
    ser.flushInput()
    print(f"Connected to {port_name} at {baud_rate} baud.")

    # Send "live" command to trigger live mode on Arduino.
    ser.write(b"live\r")
    print("Sent 'live' command to Arduino. Waiting for frames...")

    print("Starting frame capture. Press 'q' in the display window to exit.")

    while True:
        frame_buffer = read_full_frame(ser, bytes_per_frame, timeout=5)
        if frame_buffer is None:
            print("Did not receive a full frame. Retrying...")
            continue

        # If the frame is one byte extra, remove the last byte
        if len(frame_buffer) != bytes_per_frame:
            if len(frame_buffer) == bytes_per_frame + 1:
                print("Extra byte received; removing last byte.")
                frame_buffer = frame_buffer[:bytes_per_frame]
            else:
                print("Incomplete frame received:", len(frame_buffer))
                continue

        print("Total bytes received:", len(frame_buffer))
        
        # Convert the raw RGB565 data to an RGB image
        img = convert_rgb565_to_rgb(frame_buffer, camera_width, camera_height)
        
        # Display the image using OpenCV
        cv2.imshow("Frame", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ser.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
