#!/bin/bash
echo "Getting server list..."
echo ""
curl https://sks-keyservers.net/status/ | grep -E "<tr><td" | grep "http" | grep -Po '(?<=href=")[^"]*' | grep -v "/pks/lookup?op" | grep -v "info/" | grep -v ".php" | grep -v "https://" | grep -v "11371/" > servers.txt
sed -i -e 's/:11371//g' servers.txt
sed -i "s%http://%%g" "servers.txt"
echo ""
printf "Servers found in the pool on sks-keyservers.net: " && wc -l < servers.txt
echo ""
python2.7 keyserver_scan.py > sks-network.json
echo ""
printf "Servers found in the pool on sks-keyservers.net: " && wc -l < servers.txt
echo ""
echo "##########################################"
echo "# Done! Open index.html in your browser! #"
echo "##########################################"
