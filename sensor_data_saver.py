import threading
import time
from datetime import datetime

class SensorDataSaver:
    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.save_data)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def save_data(self):
        while self.running:
            # Generate a unique filename with a timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/sensor_data_{timestamp}.txt"
            
            # Open the file in append mode
            with open(filename, 'a') as file:
                # Save data every 5 minutes (60 seconds)
                time.sleep(60)
                
                # Collect all data from the queue
                while not self.data_queue.empty():
                    sensor_data = self.data_queue.get()
                    
                    # Write the data to the file
                    file.write(f"{sensor_data['timestamp']}, {sensor_data['temperature']}, {sensor_data['humidity']}\n")
                    
                    # Mark the task as done
                    self.data_queue.task_done()

            print("file logged => ", filename)