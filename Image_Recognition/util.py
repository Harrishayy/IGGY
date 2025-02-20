from datetime import datetime
import time

def generate_file_name():
    #current = datetime.now() # current date and time
    #date = current.strftime("%Y-%m-%d-%H-%M-%S") #year-month-day-hour-minute-second

    time_since_epoch = time.time()

    #file_name = f"image-{date}-{time_since_epoch}.jpg"
    file_name = f"image-{time_since_epoch}.jpg"

    return file_name