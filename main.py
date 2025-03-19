import time
from manager import Manager

# Main program
if __name__ == "__main__":
    manager = Manager()
    manager.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
        manager.stop()



'''
To separate the three classes (SensorDataCollector, SensorDataSaver, and Manager) into three separate files, you can create a Python module for each class. Here's how you can organize the code into three files:

Directory Structure
Your project directory should look like this:

Copy
project/
│
├── sensor_data_collector.py
├── sensor_data_saver.py
├── manager.py
├── main.py
How It Works:
sensor_data_collector.py:

Contains the SensorDataCollector class, which simulates collecting sensor data and putting it into a queue.

sensor_data_saver.py:

Contains the SensorDataSaver class, which saves sensor data from the queue to a file with a unique timestamp in the file name.

manager.py:

Contains the Manager class, which initializes the queue and the two classes (SensorDataCollector and SensorDataSaver).

It also provides methods to start and stop the threads.

main.py:

This is the entry point of the program. It creates an instance of the Manager class and starts the threads.

The program runs until a keyboard interrupt (Ctrl+C) is received, at which point it stops the threads gracefully.

Running the Program:
Place all four files (sensor_data_collector.py, sensor_data_saver.py, manager.py, and main.py) in the same directory.

Run the main.py file:

bash
Copy
python main.py
The program will start collecting and saving sensor data. Press Ctrl+C to stop the program.

Benefits of Separating into Files:
Modularity: Each class is in its own file, making the code easier to maintain and extend.

Reusability: You can reuse the classes in other projects by simply importing them.

Readability: The code is organized and easier to understand.

Let me know if you need further clarification!
'''