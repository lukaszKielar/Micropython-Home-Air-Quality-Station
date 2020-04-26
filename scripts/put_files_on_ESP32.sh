#!/bin/bash

set -e

for file in ./src/*
do
  ampy --port /dev/ttyUSB0 put $file
  echo "$file has been put to the board"
done

ampy --port /dev/ttyUSB0 ls
