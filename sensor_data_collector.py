import threading
import time
import random

class SensorDataCollector:
    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.collect_data)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def collect_data(self):
        while self.running:
            # Simulate sensor data (e.g., temperature, humidity, etc.)
            sensor_data = {
                'timestamp': time.time(),
                'temperature': random.uniform(20.0, 30.0),
                'humidity': random.uniform(40.0, 60.0)
            }
            
            # Put the data into the queue
            self.data_queue.put(sensor_data)
            
            # Simulate a delay between data collection
            time.sleep(1)

            print("sensor_data= ", sensor_data)