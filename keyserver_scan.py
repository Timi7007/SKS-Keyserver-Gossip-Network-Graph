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


# List of pool servers from https://sks-keyservers.net/status/ as of 2017-06-17
keyserver_domains = [
"a.keys.wolfined.com",
"a.keyserver.alteholz.eu",
"a.keyserver.pki.scientia.net",
"ams.sks.heypete.com",
"gozer.rediris.es",
"gpg.n1zyy.com",
"gpg.nebrwesleyan.edu",
"gpg.phillymesh.net",
"ice.mudshark.org",
"key.adeti.org",
"key.bbs4.us",
"key.blackbearinfosec.com",
"key1.dock23.de",
"key2.dock23.de",
"keys-02.licoho.de",
"keys.andreas-puls.de",
"keys.communityrack.org",
"keys.connectical.com",
"keys.deredvdienst.de",
"keys.digitalis.org",
"keys.drup.no",
"keys.fedoraproject.org",
"keys.flanga.io",
"keys.fspproductions.biz",
"keys.internet-sicherheit.de",
"keys.itunix.eu",
"keys.jhcloos.com",
"keys.klaus-uwe.me",
"keys.nerds.lu",
"keys.niif.hu",
"keys.schluesselbruecke.de",
"keys.sflc.info",
"keys.stueve.us",
"keys.void.gr",
"keys2.alderwick.co.uk",
"keys2.kfwebs.net",
"keyserv.sr32.net",
"keyserver.blupill.com",
"keyserver.boquet.org",
"keyserver.brian.minton.name",
"keyserver.c3l.lu",
"keyserver.cbaines.net",
"keyserver.deuxpi.ca",
"keyserver.escomposlinux.org",
"keyserver.kolosowscy.pl",
"keyserver.mattrude.com",
"keyserver.metalgamer.eu",
"keyserver.miniskipper.at",
"keyserver.nausch.org",
"keyserver.ntzwrk.org",
"keyserver.oeg.com.au",
"keyserver.opensuse.org",
"keyserver.paulfurley.com",
"keyserver.pch.net",
"keyserver.saol.no-ip.com",
"keyserver.searchy.nl",
"keyserver.secure-u.de",
"keyserver.shadowserver.org",
"keyserver.siccegge.de",
"keyserver.sincer.us",
"keyserver.skoopsmedia.net",
"keyserver.swabian.net",
"keyserver.syseleven.de",
"keyserver.timlukas.de",
"keyserver.ubuntu.com",
"keyserver.vbrandl.net",
"keyserver.vsund.de",
"keyserver.zap.org.au",
"keyserver1.computer42.org",
"keyserver1.gnupg.pub",
"keyserver2.boquet.org",
"keyserver2.computer42.org",
"klucze.achjoj.info",
"pgp-srv.deib.polimi.it",
"pgp.archreactor.org",
"pgp.gwolf.org",
"pgp.h-ix.net",
"pgp.key-server.io",
"pgp.lehigh.edu",
"pgp.mit.edu",
"pgp.net.nz",
"pgp.surfnet.nl",
"pgp.uni-mainz.de",
"pgp.uplinklabs.net",
"pgpkeys.co.uk",
"pgpkeys.eu",
"pgpkeys.mallos.nl",
"pgpkeys.urown.net",
"pgpkeyserver.nl",
"schluesselkasten.wertarbyte.de",
"sks.b4ckbone.de",
"sks.bonus-communis.eu",
"sks.bootc.eu",
"sks.daylightpirates.org",
"sks.es.net",
"sks.fidocon.de",
"sks.karotte.org",
"sks.labs.nic.cz",
"sks.mbk-lab.ru",
"sks.mj2.uk",
"sks.neel.ch",
"sks.okoyono.de",
"sks.openpgp-keyserver.de",
"sks.rarc.net",
"sks.spodhuis.org",
"sks.srv.dumain.com",
"sks.stsisp.ro",
"sks.undergrid.net",
"sks.ustclug.org",
"vanunu.calyxinstitute.org",
"vm-keyserver.spline.inf.fu-berlin.de",
"zimmermann.mayfirst.org",
"zuul.rediris.es",
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
        
