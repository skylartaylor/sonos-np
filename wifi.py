#!/usr/local/bin/python3
import sys
from sonos import get_net

if __name__ == "__main__":
    stats = get_net()
    print("w: {} {}%".format(stats['SSID'].lower(), stats["sigstrength"]))
