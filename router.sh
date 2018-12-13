#!/bin/bash
if [ -z $2 ]; then
    echo "Sao necessarios ao menos 2 parametros!"
    echo "Formato: servidor tempo [arquivo]"
    exit
else
    if [ -z $3 ]; then
        ./code/dist/router/router $1 $2;
    else
        ./code/dist/router/router $1 $2 $3;
    fi
fi
