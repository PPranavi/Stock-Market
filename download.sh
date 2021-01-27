#!/bin/bash

for (( i=0; i<60; i++ )) 
do
    file="yahoo_$(date +%Y_%m_%d_%H_%M_%S).html"
    
    wget -O $file "https://finance.yahoo.com/most-active"
    
    java -jar tagsoup-1.2.jar --files $file
    
    xfn=${file/.html/.xhtml}

    python3 extract.py $xfn

    rm $file
    rm $xfn

    sleep 60
done