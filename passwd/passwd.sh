#!/bin/bash

pComplexity=$1
pLength=$2
charSet=""

if [[ -z "$pLength" ]];then
 pLength=10
fi

if [[ $pComplexity == 1 ]]; then 
 charSet="A-Za-z"
elif [[ $pComplexity == 2 ]]; then
 charSet="A-Za-z0-9"
elif [[ $pComplexity == 3 ]]; then
 charSet='A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~'
else
 charSet='A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~'
fi

tr -dc $charSet </dev/urandom | head -c $pLength;echo ''
