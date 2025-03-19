import queue
from sensor_data_collector import SensorDataCollector
from sensor_data_saver import SensorDataSaver

class Manager:
    def __init__(self):
        self.data_queue = queue.Queue()
        self.collector = SensorDataCollector(self.data_queue)
        self.saver = SensorDataSaver(self.data_queue)

    def start(self):
        self.collector.start()
        self.saver.start()

    def stop(self):
        self.collector.stop()
        self.saver.stop()