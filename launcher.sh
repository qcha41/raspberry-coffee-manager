#!/bin/bash
date
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/local/bin/python3.6 launcher.py