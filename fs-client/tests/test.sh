#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path>"
    exit 1
fi

path_string="$1"

while true; do
    echo "Please select an option:"
    echo "1. Run ALL tests"
    echo "2. Run INTEGRATION tests"
    echo "3. RUN UNIT tests"
    echo "4. Quit"

    read -p "Enter your choice [1-4]: " choice

    case $choice in
        1)
            echo "You selected Option 1."
            cd integration/
            pytest int_server.py
            pytest int_boundarycase.py
            pytest int_errorhandling.py

            cd .. && cd unit
            pytest unit_client.py
            pytest unit_argparse.py
            pytest unit_errorhandling.py
            cd ..
            ;;
        2)
            echo "You selected Option 2."
            cd integration/
            pytest int_server.py
            pytest int_boundarycase.py
            pytest int_errorhandling.py
            cd ..
            ;;
        3)
            echo "You selected Option 3."
            cd unit
            pytest unit_client.py
            pytest unit_argparse.py
            pytest unit_errorhandling.py
            cd ..
            ;;
        4)
            echo "Exiting the program. Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
    echo    # Print a blank line for better readability
done

