#!/bin/bash

set_model_dir=$(realpath $(dirname $0))
model_name="$1"
target_model_file="$set_model_dir/Modelfile"

#if ! [[ -d $set_model_dir/babelicamodels ]]; then mkdir $set_model_dir/babelicamodels; fi


params=$(echo "PARAMETER temperature $2")


echo "FROM $model_name" > $target_model_file
echo >> $target_model_file
echo "$params" >> $target_model_file
echo >> $target_model_file
echo "SYSTEM \"\"\"" >> $target_model_file
echo "$3" >> $target_model_file
echo "\"\"\"" >> $target_model_file

if [[ -f $target_model_file ]]; then
    echo "File exists: $target_model_file"
    echo "Contents:"
    echo "$(cat $target_model_file)"
    
    ollama create babellica -f "$target_model_file"
    rm $target_model_file
else
    echo "file $target_model_file does not exist. Exiting"
    exit
fi

