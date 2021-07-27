#!/bin/bash

if [ $# -le 3 ]
then
    echo "Usage:rowsplit.sh source.csv iteratorfile.csv label targetdir [slurmarrayID]"
    echo "  iteratorfile.csv: The first column of iteratorfile will be used to performa rowsplit on source.csv"
    echo "  label: Field Label from first row"
    echo "  targetdir: location to place new files"
    echo "  Eg: rowsplit.sh bigfile.csv list-of-vals.csv 0002 ~/targetdir"
    echo "  If slurmarrayID is passed, only the nth row of iteratorfile.csv is used (nth row is slurmarrayID)"
    echo "  Dependencies: csvkit/utilities must be in PATH"
    exit
    
fi
#ITERATOR="`dirname \"$0\"`/../plugins/levman/segmentMap.csv"
BIGFILE=$1
ITERATOR=$2
LABEL=$3
TARGET=$4
SLURMARRAYID=$5

COL=`head -1 $BIGFILE|tr , '\n' |grep --line-number "^$LABEL$"|cut -d: -f1`

if [[ $COL -eq "" ]];then
  echo "Label Not Found ($LABEL)"
  exit
fi
CSVGREP=`which csvgrep.py|wc -l`
if [[ $CSVGREP -eq 0 ]];then
  echo "csvgrep.py not found in path.  Please install csvkit and add csvkit/utilities to your path"
fi
COUNTER=0
while read p; do
    roi=$(echo $p |cut -d"," -f1)
    [[ $roi =~ ^#.* ]] && continue    #Skip comments
    let COUNTER++
    if [[ $SLURMARRAYID -eq "" || $SLURMARRAYID -eq $COUNTER ]];then
      echo "Searching for $roi"
    fi
    csvgrep.py -c $COL -m $roi $BIGFILE > "$TARGET/$roi.csv" & 

done <$ITERATOR