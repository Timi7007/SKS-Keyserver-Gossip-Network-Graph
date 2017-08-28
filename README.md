# SKS Keyserver Gossip Network Graph
*SKS/GPG Keyserver Gossip Network Graph forked from https://gist.github.com/diafygi/3f344c22f8a37a7b2151*

**Generating an Edge Bundling visualization of the SKS keyserver gossip network.**

Written by Daniel Roesler (https://daylightpirates.org/)

Released under GPLv3.

Updated by Timlukas Bloch (https://timlukas.de)

Uses data from https://sks-keyservers.net

## Prerequisites:
* Internet connection
* Browser
* echo, grep, sed
* curl (tested on 7.47)
* Python (2.7 or higher)

## Usage:
* Run run.sh: `./run.sh`
* Open index.html in your browser.

**Mouseover any of the nodes in the network to see the incoming links (dependants) in green and the outgoing links (dependencies) in red.**

## Original README:
~~~
This is a quick script to scan the SKS keyserver pool and build
a Edge Bundling visualization of the gossip network.
How to use:
1. Update the keyserver_domains list below with the keyservers to scan.
2. Run: python keyserver_scan.py > sks-network.json
3. Open index.html in your browser!
Written by Daniel Roesler (https://daylightpirates.org/)
Released under GPLv3.

Mouseover any of the nodes in this network to see the incoming links (dependants) in green and the outgoing links (dependencies) in red.

See the visualization: http://bl.ocks.org/diafygi/3f344c22f8a37a7b2151
~~~
