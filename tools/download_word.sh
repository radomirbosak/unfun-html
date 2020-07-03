#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 WORD"
    exit 1
fi

WORD=$1

mkdir -p data tests/data

wget "https://www.duden.de/rechtschreibung/$WORD" -O "data/$WORD.html"
duden $WORD --export > "data/$WORD.yaml"
cp "data/$WORD.yaml" "data/$WORD.html" tests/data
