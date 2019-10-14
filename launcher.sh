#!/bin/bash
export DISPLAY=:0
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
sudo python3 initialize.py
read