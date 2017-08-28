"""
This is a quick script to scan the SKS keyserver pool and build
a Edge Bundling visualization of the gossip network.

How to use:
1. Start run.sh
2. Open index.html in your browser!

Written by Daniel Roesler (https://daylightpirates.org/)
Released under GPLv3.
Updated by Timlukas Bloch (https://timlukas.de)
"""
import urllib2, time, sys, re, collections, json, datetime, tzlocal

server_list_path = 'servers.txt'
server_list = open(server_list_path,'r')

keyserver_domains = server_list.read().splitlines()

server_list.close()

keyserver_peers = {}
keyserver_retries = collections.defaultdict(int)
i = 0
while i < len(keyserver_domains):
    domain = keyserver_domains[i]

    sys.stderr.write("Requesting peers for {}...".format(domain))
    try:
        url = "http://{}:11371/pks/lookup?op=stats".format(domain)
        req = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        if keyserver_retries[domain] < 10:
            keyserver_retries[domain] += 1
            sys.stderr.write("failed, retrying {}/10...\n".format(keyserver_retries[domain]))
            continue
        else:
            sys.stderr.write("failed, skipping...\n")
            i += 1
            continue

    html = req.read()
    peers_html = re.search("<table summary=\"Gossip Peers\">(.*?)</table>",
        html, re.MULTILINE|re.DOTALL).group(1)
    peers = re.findall("<tr><td>([\w\.]+) [\d]+</td></tr>", peers_html)
    for p in peers:
        keyserver_peers.setdefault(domain, []).append(p)
    sys.stderr.write("found {} peers\n".format(len(peers)))
    i += 1

result = []
all_peers = set()
for n, domain in enumerate(sorted(keyserver_peers.keys())):
    result.append({
        "name": domain,
        "size": n + 1,
        "peers": keyserver_peers[domain],
    })
    for p in keyserver_peers[domain]:
        all_peers.add(p)

len_domains = len(keyserver_peers.keys())
for n, peer in enumerate(sorted(list(all_peers))):
    if peer not in keyserver_peers:
        result.append({
            "name": peer,
            "size": n + len_domains + 1,
            "peers": [],
        })

print json.dumps(result, indent=4, sort_keys=True)



timestamp_path = 'timestamp.html'
timestamp_file = open(timestamp_path,'w')

now = datetime.datetime.now(tzlocal.get_localzone())
print >> timestamp_file, ('Last Update: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + " " + now.strftime('%Z'))

timestamp_file.close()
