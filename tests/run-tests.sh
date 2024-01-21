#!/bin/bash

set -e

echo "./test_create_user.py"
python test_create_user.py

for filename in ./*.py; do
	if [ "$filename" != "./test_create_user.py" ]; then
		printf "\n\n${filename}\n"
		python $filename
	fi
done