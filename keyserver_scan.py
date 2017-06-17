"""
This is a quick script to scan the SKS keyserver pool and build
a Edge Bundling visualization of the gossip network.

How to use:
1. Update the keyserver_domains list below with the keyservers to scan.
2. Run: python keyserver_scan.py > sks-network.json
3. Open index.html in your browser!

Written by Daniel Roesler (https://daylightpirates.org/)
Released under GPLv3.
"""
import urllib2, time, sys, re, collections, json


# List of pool servers from https://sks-keyservers.net/status/ as of 2015-09-01
keyserver_domains = [
    "a.keyserver.pki.scientia.net",
    "ams.sks.heypete.com",
    "b.key.ip6.li",
    "gpg.n1zyy.com",
    "gpg.nebrwesleyan.edu",
    "key.adeti.org",
    "key.cccmz.de",
    "key.ip6.li",
    "keys-01.licoho.de",
    "keys-02.licoho.de",
    "keys.alderwick.co.uk",
    "keys.andreas-puls.de",
    "keys.connectical.com",
    "keys.digitalis.org",
    "keys.exosphere.de",
    "keys.fedoraproject.org",
    "keys.i2p-projekt.de",
    "keys.internet-sicherheit.de",
    "keys.itunix.eu",
    "keys.jhcloos.com",
    "keys.nerds.lu",
    "keys.niif.hu",
    "keys.riverwillow.net.au",
    "keys.schluesselbruecke.de",
    "keys.sflc.info",
    "keys.stueve.us",
    "keys.techwolf12.nl",
    "keys2.kfwebs.net",
    "keyserver.adamas.ai",
    "keyserver.bdr.net.pl",
    "keyserver.blazrsoft.com",
    "keyserver.blupill.com",
    "keyserver.br.nucli.net",
    "keyserver.c3l.lu",
    "keyserver.cbaines.net",
    "keyserver.codinginfinity.com",
    "keyserver.compbiol.bio.tu-darmstadt.de",
    "keyserver.computer42.org",
    "keyserver.dacr.hu",
    "keyserver.durcheinandertal.ch",
    "keyserver.eddiecornejo.com",
    "keyserver.erat.systems",
    "keyserver.globale-gruppe.de",
    "keyserver.kjsl.com",
    "keyserver.kolosowscy.pl",
    "keyserver.leg.uct.ac.za",
    "keyserver.lsuhscshreveport.edu",
    "keyserver.matteoswelt.de",
    "keyserver.mattrude.com",
    "keyserver.mesh.deuxpi.ca",
    "keyserver.metalgamer.eu",
    "keyserver.nausch.org",
    "keyserver.nucli.net",
    "keyserver.oeg.com.au",
    "keyserver.pch.net",
    "keyserver.pkern.at",
    "keyserver.searchy.nl",
    "keyserver.secretresearchfacility.com",
    "keyserver.secure-u.de",
    "keyserver.siccegge.de",
    "keyserver.skoopsmedia.net",
    "keyserver.ubuntu.com",
    "keyserver.za.nucli.net",
    "keyserver.zap.org.au",
    "klucze.achjoj.info",
    "openpgp-keyserver.eu",
    "openpgp.andrew.kvalhe.im",
    "openpgp.us",
    "pgp.archreactor.org",
    "pgp.benny-baumann.de",
    "pgp.gwolf.org",
    "pgp.h-ix.net",
    "pgp.key-server.io",
    "pgp.mit.edu",
    "pgp.net.nz",
    "pgp.ohai.su",
    "pgp.rediris.es",
    "pgpkey.org",
    "pgpkeys.co.uk",
    "pgpkeys.eu",
    "pgpkeys.urown.net",
    "pks.aaiedu.hr",
    "sks.alpha-labs.net",
    "sks.b4ckbone.de",
    "sks.bootc.eu",
    "sks.daylightpirates.org",
    "sks.es.net",
    "sks.fidocon.de",
    "sks.gpg.im",
    "sks.karotte.org",
    "sks.labs.nic.cz",
    "sks.mrball.net",
    "sks.muc.drweb-av.de",
    "sks.openpgp-keyserver.de",
    "sks.pkqs.net",
    "sks.rainydayz.org",
    "sks.research.nxfifteen.me.uk",
    "sks.spodhuis.org",
    "sks.srv.dumain.com",
    "sks.static.lu",
    "vm-keyserver.spline.inf.fu-berlin.de",
    "zimmermann.mayfirst.org",
]

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
        
