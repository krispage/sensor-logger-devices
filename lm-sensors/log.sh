#!/bin/bash

pushd /var/scripts/sensors/
python3 log.py >> /var/log/logger.log
python3 process-fails.py >> /var/log/process-failed-logs.log
popd
