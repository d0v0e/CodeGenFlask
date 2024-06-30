#!/bin/bash

host="0.0.0.0"
port=5000

while getopts ":h:p:" opt; do
  case $opt in
    h)
      host=$OPTARG
      ;;
    p)
      port=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      echo "Usage: ./$0 [-h <host>] [-p <port>]"
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      echo "Usage: ./$0 [-h <host>] [-p <port>]"
      ;;
  esac
done

# if your number of GPU >= 1, you can use the command below to set the first NAVIDIA GPU as default 
# export MESA_D3D12_DEFAULT_ADAPTER_NAME=NAVIDIA

# run flask app
export FLASK_APP=app.py
export FLASK_RUN_HOST=$host
export FLASK_RUN_PORT=$port
flask run