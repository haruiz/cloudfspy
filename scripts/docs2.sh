#!/bin/bash
# define a format variable


echo "Converting all notebooks to $2 in $1"

find "$1" -name "*.ipynb" -not -path "*/.venv/*" -not -path "*/.git/*" \
| while read notebook; do
    dir=$(dirname $notebook)
     # convert all notebooks to python scripts
     echo "Converting $notebook to python script in $dir"
     jupyter nbconvert --to "$2" --output-dir $dir $notebook
done

