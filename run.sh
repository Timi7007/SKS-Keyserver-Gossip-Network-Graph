#!/bin/bash
echo "Be sure to update the keyserver_domains list in keyserver_scan.py with the keyservers form the pool."
python keyserver_scan.py > sks-network.json
echo "Done! Open index.html in your browser!"
