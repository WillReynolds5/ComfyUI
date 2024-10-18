#!/bin/bash

# Loop that continuously runs the python script
while true
do
    # Run the python script
    python main.py --listen

    # Check the exit status of the script
    if [ $? -ne 0 ]; then
        echo "The script failed or was killed, restarting..."
    fi

    # Optionally wait a moment before restarting
    sleep 1
done
