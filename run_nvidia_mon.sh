#!/bin/bash

# Get the absolute path of the script directory
script_dir="$(cd "$(dirname "$0")" && pwd)"

# Run the Python script in the background with nohup from the script directory
nohup python3 "${script_dir}/nvidia-mon.py" &

# Wait for .1 milliseconds
sleep 0.00001

# Close the terminal
exit
