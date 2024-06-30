#!/bin/bash

source ./env/py3-11_env/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# check the devices in your system
python device_check.py

# test the environment
python test.py