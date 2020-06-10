#!/bin/bash
export DISPLAY=:0
date
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
python3.6 launcher.py