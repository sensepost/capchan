#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: ./command_runner_wunner.sh <command> <count>"
  exit 1
fi

command=$1
count=$2

if ! [[ $count =~ ^[0-9]+$ ]]; then
  echo "Error: Count must be a positive integer."
  exit 1
fi

for ((i=1; i<=$count; i++))
do
  echo "Iteration: $i"
  echo "Running command: $command"
  eval $command
  echo ""
done

