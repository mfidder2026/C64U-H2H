#!/usr/bin/env python3
"""
Builds the C64 Ultimate link test: build/linktest.prg and build/linktest.d64.

    python build.py            build (needs cc65; the disk also needs VICE's c1541)
    python build.py run        build and start it in VICE with an RR-Net cartridge
                               (the host network adapter: the environment variable NPCAP_IF)

cc65 and VICE are found through CC65_BIN and VICE_DIR (their bin folders), else on the PATH.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
SRC = os.path.join(HERE, "src")


def tool(name: str, env: str) -> str:
    folder = os.environ.get(env)
    if folder:
        for ext in ("", ".exe"):
            path = os.path.join(folder, name + ext)
            if os.path.isfile(path):
                return os.path.normpath(path)       # cl65 finds its tools next to itself
    path = shutil.which(name)
    if not path:
        sys.exit(f"{name} not found: put it on the PATH or set {env} to its folder")
    return os.path.normpath(path)


def build() -> str:
    os.makedirs(BUILD, exist_ok=True)
    prg = os.path.join(BUILD, "linktest.prg")
    subprocess.run([tool("cl65", "CC65_BIN"), "-t", "c64", "-O", "-o", prg, "-m", os.path.join(BUILD, "linktest.map"),
                    *(os.path.join(SRC, f) for f in ("main.c", "timer.s", "uci.s", "rrnet.s"))],
                   check=True, cwd=BUILD)
    d64 = os.path.join(BUILD, "linktest.d64")
    subprocess.run([tool("c1541", "VICE_DIR"), "-format", "link test,lt", "d64", d64, "-write", prg, "linktest"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"built build/linktest.prg ({os.path.getsize(prg)} bytes) and build/linktest.d64")
    return d64


if __name__ == "__main__":
    disk = build()
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        iface = os.environ.get("NPCAP_IF")
        if not iface:
            sys.exit("set NPCAP_IF to the network adapter for the RR-Net cartridge (VICE: Settings, Ethernet)")
        subprocess.Popen([tool("x64sc", "VICE_DIR"), "-ethernetcart", "-ethernetcartmode", "1",
                          "-ethernetioif", iface, "-autostart", disk])
