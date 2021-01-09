#!/bin/bash
fshift() { local v n=$'\n';read -r v < <(
    sed -e $'1{w/dev/stdout\n;d}' -i~ "$1")
    printf ${2+-v} $2 "%s${n[${2+2}]}" "$v"
}

fpop() { local v n=$'\n';read -r v < <(
    sed -e $'${w/dev/stdout\n;d}' -i~ "$1")
    printf ${2+-v} $2 "%s${n[${2+2}]}" "$v"
}
printf "Line #%2d\n" {3..12} > file

fshift file patID

echo "the patient is $patID"



