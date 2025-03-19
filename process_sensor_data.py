import os
import time
import glob

# import socket
# if not hasattr(socket, '_GLOBAL_DEFAULT_TIMEOUT'):
#     socket._GLOBAL_DEFAULT_TIMEOUT = object()

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration
DATA_DIR = "data"  # Directory where sensor data files are stored
PROCESSED_DIR = "processed_data"  # Directory to move processed files
INFLUXDB_URL = "http://localhost:8086"  # InfluxDB URL
INFLUXDB_TOKEN = "Ht7Q8Ph4ms3C78BEsZyTNIcrYOw39n-bgXMvxamRqy98MpWJo-9TQPQNKPcYaTR1XSat1k6pLEs7rLlWlsCrHQ=="  # InfluxDB token
INFLUXDB_ORG = "guowork"  # InfluxDB organization
INFLUXDB_BUCKET = "sensor_data"  # InfluxDB bucket

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def get_oldest_file(directory):
    """Get the oldest file in the directory."""
    files = glob.glob(os.path.join(directory, "*.txt"))
    if not files:
        return None
    return min(files, key=os.path.getctime)

def insert_data_into_influxdb(file_path):
    """Insert data from the file into InfluxDB."""
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    try:
        with open(file_path, "r") as file:
            for line in file:
                timestamp, temperature, humidity = line.strip().split(", ")
                
                # Create a data point for InfluxDB
                point = Point("sensor_reading") \
                    .tag("sensor", "sensor_1") \
                    .field("temperature", float(temperature)) \
                    .field("humidity", float(humidity)) \
                    .time(int(float(timestamp)), WritePrecision.S)

                # Write the point to InfluxDB
                write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)

        print(f"Data from {file_path} inserted into InfluxDB.")
    except Exception as e:
        print(f"Error inserting data into InfluxDB: {e}")
    finally:
        client.close()

def move_file_to_processed(file_path):
    """Move the processed file to the 'processed_data' directory."""
    filename = os.path.basename(file_path)
    destination = os.path.join(PROCESSED_DIR, filename)
    os.rename(file_path, destination)
    print(f"Moved {file_path} to {destination}.")

def process_files():
    """Process the oldest file in the data directory."""
    oldest_file = get_oldest_file(DATA_DIR)
    if oldest_file:
        print(f"Processing file: {oldest_file}")
        insert_data_into_influxdb(oldest_file)
        move_file_to_processed(oldest_file)
    else:
        print("No files to process.")

if __name__ == "__main__":
    process_files()



'''
Certainly! Below is a Python script that checks for data files every 15 minutes (using a cron job), loads the oldest data file, inserts the data into InfluxDB, and then moves the processed file to another folder.

Explanation of the Script:
Configuration:

DATA_DIR: Directory where sensor data files are stored.

PROCESSED_DIR: Directory to move processed files.

InfluxDB connection details (INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET).

Functions:

get_oldest_file(directory): Finds the oldest file in the specified directory.

insert_data_into_influxdb(file_path): Reads the file, parses the data, and inserts it into InfluxDB.

move_file_to_processed(file_path): Moves the processed file to the processed_data directory.

process_files(): Orchestrates the process of finding the oldest file, inserting its data into InfluxDB, and moving it to the processed_data directory.

InfluxDB Integration:

Uses the influxdb_client library to write data to InfluxDB.

Each line in the file is parsed into a timestamp, temperature, and humidity, and written as a data point.

File Handling:

The script ensures that the data and processed_data directories exist.

After processing, the file is moved to the processed_data directory to avoid reprocessing.

Setting Up the Cron Job
To run this script every 15 minutes, you can set up a cron job on a Unix-based system (Linux/Mac).

Open the crontab editor:

bash
Copy
crontab -e
Add the following line to schedule the script to run every 15 minutes:

bash
Copy
*/15 * * * * /usr/bin/python3 /path/to/process_sensor_data.py
Replace /path/to/process_sensor_data.py with the full path to your script.

Save and exit the crontab editor.

Directory Structure
After setting up the script and cron job, your project directory should look like this:

Copy
project/
│
├── data/
│   ├── sensor_data_20231025_143000.txt
│   ├── sensor_data_20231025_143500.txt
│   └── ...
│
├── processed_data/
│   ├── sensor_data_20231025_143000.txt
│   ├── sensor_data_20231025_143500.txt
│   └── ...
│
├── process_sensor_data.py
How It Works:
The cron job runs the process_sensor_data.py script every 15 minutes.

The script checks the data directory for the oldest file.

It reads the file, inserts the data into InfluxDB, and moves the file to the processed_data directory.

If no files are found, the script does nothing.

Dependencies:
Install the influxdb-client library:

bash
Copy
pip install influxdb-client
Ensure InfluxDB is running and accessible at the specified URL.

This setup ensures that your sensor data is processed, stored in InfluxDB, and archived systematically. Let me know if you need further assistance!

'''