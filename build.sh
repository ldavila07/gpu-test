#!/bin/bash

wget http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar
tar -xvf images.tar
wget http://vision.stanford.edu/aditya86/ImageNetDogs/annotation.tar
tar -xvf annotation.tar
python gen-images.py  ./Images/ ./Annotation/