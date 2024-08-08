#!/bin/bash
for i in {1..100}; do
    echo -----$i
    python3 tasks_jerkmate_noreg.py
    #sleep 60
done
#python3 tasks_jerkmate.py
#sleep 300
