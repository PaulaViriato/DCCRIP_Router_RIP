#!/bin/bash

cd code;
pyinstaller router.py;
rm -rf build;
rm -rf __pycache__;
rm router.spec;
cd ..;
chmod 777 router.sh;

