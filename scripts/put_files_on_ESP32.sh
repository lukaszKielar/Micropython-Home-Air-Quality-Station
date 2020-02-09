#!/bin/bash

set -e

for file in "$@"
do
  ampy --port /dev/ttyUSB0 put src/$file
  echo "$file has been put to the board"
done

ampy --port /dev/ttyUSB0 ls
