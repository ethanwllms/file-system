#bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
yes Y | pip uninstall websocket 
yes Y | pip uninstall websocket-client 
pip install websocket-client