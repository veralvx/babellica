#!/bin/bash

if [[ $5 == "llm" ]] || [ -z "$5" ]; then
    ollama serve & sleep 2
fi

startup_dir=$(realpath $(dirname $0))

$startup_dir/babellica.sh $1 $2 $3 $4 $5 $6