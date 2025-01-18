## Running Pytest Tests with test.sh
### Overview
This document provides instructions on how to run test suites using pytest along with the helper shell script test.sh. The script lets you specify which test suites to execute.

### Prerequisites
- Python Installed: Ensure Python 3.x is installed on your system.

- pytest Installed: You can install pytest using pip if it's not already installed. Run:

```
pip install pytest
```

- test.sh Script: Ensure you have the test.sh script in your project directory. This script enables you to select which test suites to run.

    - IMPORTANT! tests/integration/int_server.py needs to have the path updated within the test_create_directory function to reflect local file path, you can paste in the path from the allowed directories output from the server process.

- start the file-system server

### Directory Structure
Here's an example of how your project directory might be structured:

file-system/
├── fs-client/
|    ├── fs-client/
|       ├──tests/
|           ├──integration/    
│               ├── int_server.py
│               ├── int_errorhandling.py
│               └── int_boundarycases.py
│
|            ├──unit/    
│               ├── unit_client.py
│               ├── unit_errorhandling.py
│               └── unit_argparse.py
|
#### Using test.sh
The test.sh script allows you to run specific test suites based on your selection. Here’s how to use it:

##### Step 1: Open a Terminal
Navigate to your project directory using the command line.

##### Step 2: Make the Script Executable
Before running the script, ensure it is executable. You can set the correct permissions by running:

```
chmod +x test.sh
```

##### Step 3: Run the Script
Execute the test.sh script with options. You can typically run:

```
./test.sh
```

##### Step 4: Choose Options
The test.sh script should prompt you with available options (test suites). Depending on its configuration, you might see something like:

```
Please select an option:
1. Run ALL tests
2. Run INTEGRATION tests
3. RUN UNIT tests
4. Quit
Enter your choice [1-4]:
```

##### Step 5: Input your Choice
You can input the number corresponding to the test suite you want to run. If you select "Run All Tests," the script will execute all available tests in the tests/ directory.

##### Step 6: Review the Results
After running the selected tests, pytest will display the results in your terminal. You will see output indicating which tests passed, failed, or were skipped.

### Troubleshooting

- pytest not found: If you receive an error indicating that pytest is not found, ensure that it is correctly installed and accessible in your PATH.

- Permission Denied: If you receive a "permission denied" error while trying to execute test.sh, ensure you have made the script executable with the chmod +x test.sh command.

### Conclusion
By using pytest alongside the test.sh script, you can effectively manage and run your test suites based on your current testing needs. This method provides greater flexibility and organization to your testing workflow.