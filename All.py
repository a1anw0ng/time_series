import threading
import queue
import time
import random
from datetime import datetime

# Simulate sensor data collection
def collect_sensor_data(data_queue):
    while True:
        # Simulate sensor data (e.g., temperature, humidity, etc.)
        sensor_data = {
            'timestamp': time.time(),
            'temperature': random.uniform(20.0, 30.0),
            'humidity': random.uniform(40.0, 60.0)
        }
        
        # Put the data into the queue
        data_queue.put(sensor_data)
        
        # Simulate a delay between data collection
        time.sleep(1)

        print("sensor_data= ", sensor_data)

# Save sensor data to a file every 5 minutes
def save_sensor_data(data_queue):
    while True:
        # Generate a unique filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/sensor_data_{timestamp}.txt"

        # Open the file in append mode
        with open(filename, 'a') as file:
            # Save data every 1 minutes (60 seconds)
            time.sleep(60)
            
            # Collect all data from the queue
            while not data_queue.empty():
                sensor_data = data_queue.get()
                
                # Write the data to the file
                file.write(f"{sensor_data['timestamp']}, {sensor_data['temperature']}, {sensor_data['humidity']}\n")
                
                # Mark the task as done
                data_queue.task_done()

# Create a queue to hold the sensor data
data_queue = queue.Queue()

# Create and start the sensor data collection thread
collector_thread = threading.Thread(target=collect_sensor_data, args=(data_queue,))
collector_thread.daemon = True
collector_thread.start()

# Create and start the data saving thread
saver_thread = threading.Thread(target=save_sensor_data, args=(data_queue,))
saver_thread.daemon = True
saver_thread.start()

# Keep the main program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated.")