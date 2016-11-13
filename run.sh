#!/usr/bin/env bash

# Run script for fraud detection algorithm with a python file
# Following example from https://github.com/InsightDataScience/digital-wallet/blob/master/run.sh

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
