#!/bin/bash

cd code;
pyinstaller router.py;
pyinstaller router_review.py;
rm -rf build;
rm -rf __pycache__;
rm router.spec;
rm router_review.spec;
cd ..;
chmod 777 router.sh;
chmod 777 router_review.sh;

