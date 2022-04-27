#!/bin/bash --login
echo "____________________________________________"
echo "Checkout to latest tag in ART"
echo "____________________________________________"
git checkout v4.15.4 -f
echo "____________________________________________"
echo "Describing Head"
echo "____________________________________________"
git describe > HEAD
echo "____________________________________________"
echo "Making changes to application.json"
echo "____________________________________________"
cp application.json.example application.json
echo "____________________________________________"
