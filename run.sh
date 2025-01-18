#bin/bash

python3 fs-client/main.py --host 0.0.0.0 --port 8765 read --path /users/ethanwilliams/documents/code/file-system/fs-test/hello_there.txt
python3 fs-client/main.py --host 0.0.0.0 --port 8765 write --path /users/ethanwilliams/documents/code/file-system/fs-test/hello_there1.txt --content "oh, hello there"
python3 fs-client/main.py --host 0.0.0.0 --port 8765 search --path /users/ethanwilliams/documents/code/file-system/fs-test/ --pattern "hel"
python3 fs-client/main.py --host 0.0.0.0 --port 8765 list --path /users/ethanwilliams/documents/code/file-system/fs-test
python3 fs-client/main.py --host 0.0.0.0 --port 8765 create_dir --path /users/ethanwilliams/documents/code/file-system/fs-test/new1