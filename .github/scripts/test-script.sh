#bin/bash

cd ../../fs-client/tests/integration/
pytest int_server.py
pytest int_boundarycase.py
pytest int_errorhandling.py

cd .. && cd unit
pytest unit_client.py
pytest unit_argparse.py
pytest unit_errorhandling.py