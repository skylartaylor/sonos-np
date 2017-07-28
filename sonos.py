#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from soco import SoCo
from soco.discovery import discover
import json
import os
import math
import subprocess
import argparse

def get_net():
    airport = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'])
    stats = {}

    for line in airport.split(b'\n'):
        line = line.lstrip().split(b': ',2)
        if len(line) < 2:
            continue
        stats[line[0].decode()] = line[1].decode()

    stats["sigstrength"] = min(max(2 * (int(stats['agrCtlRSSI']) + 100), 0), 100)
    return stats

def load_players(force=False):
    players = {"players":{}}
    if os.path.exists("/tmp/players"):
        players = json.load(open("/tmp/players"))

    ssid = get_net()["SSID"]
    if force or ssid != players.get("ssid"):
        players["players"] = {}
        players["ssid"] = ssid

        devices = discover(timeout=10) or []
        for device in devices:
            players["players"][device.player_name] = device.ip_address
        json.dump(players, open("/tmp/players", "w"))

    return players

def by_name(name):
    """Return a device by name.
    Args:
        name (str): The name of the device to return.
    Returns:
        :class:`~.SoCo`: The first device encountered among all zone with the
            given player name. If none are found `None` is returned.
    """
    players = load_players()
    if name in players["players"]:
        player = SoCo(players["players"][name])
        if player.group:
            return player.group.coordinator

def set_speaker(name):
    players = {}
    if os.path.exists("/tmp/players"):
        players = json.load(open("/tmp/players"))
    players['current'] = name
    json.dump(players, open("/tmp/players", "w"))

name_maps = {
    'bedroom': 'bed'
}

def map_name(name):
    name = name.lower()
    if name not in name_maps:
        name = ''.join([ c[0] for c in name.split() ])
    else:
        name = name_maps.get(name)
    return name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--play", help="Play Sonos.", action="store_true")
    parser.add_argument("--pause", help="Pause Sonos.", action="store_true")
    parser.add_argument("--next", help="Go forward in the queue.", action="store_true")
    parser.add_argument("--previous", help="Go back in the queue.", action="store_true")
    parser.add_argument("--set", help="Set default speaker.", action="store_true")
    parser.add_argument("--list", help="List players.", action="store_true")
    parser.add_argument("--force", help="Force cache update.", action="store_true")
    parser.add_argument("speaker", help="Play Sonos.", nargs='?')
    args = parser.parse_args()

    current = args.speaker or load_players(force=args.force).get("current") or "Living Room"

    device = by_name(current)
    if not device:
        quit()

    if args.set:
        set_speaker(current)
    elif args.play:
        device.play()
    elif args.pause:
        device.pause()
    elif args.next:
        device.next()
    elif args.previous:
        device.previous()
    elif args.list:
        devices = discover(timeout=10) or []
        for device in devices:
            print(device.get_speaker_info())
    else:
        track = None
        if device.is_playing_tv:
            track = 'TV'
        elif device.get_current_transport_info()['current_transport_state'] == 'PLAYING':
            track = device.get_current_track_info()
            track = '{} - {}'.format(track['title'], track['artist'])

        players = load_players()["players"]

        if track:
            devices = [device]
            for player in device.group.members:
                if player == device:
                    continue
                if player.player_name in players and players[player.player_name] == player.ip_address:
                    devices.append(player)
            print("{}: {}".format('+'.join([map_name(d.player_name) for d in devices]), track.lower()))
        else:
            print("sonos")

        print("---")
        for player in players:
            print('{} |bash=/Users/skylartaylor/bitbar/sonos/sonos.py param1="--set" param2="{}" terminal=false refresh=true'.format(player, player))

        print('play |color=green bash=/Users/skylartaylor/bitbar/sonos/sonos.py param1="--play" terminal=false refresh=true')
        print('pause |color=green bash=/Users/skylartaylor/bitbar/sonos/sonos.py param1="--pause" terminal=false refresh=true')
        print('previous |color=green bash=/Users/skylartaylor/bitbar/sonos/sonos.py param1="--previous" terminal=false refresh=true')
        print('next |color=green bash=/Users/skylartaylor/bitbar/sonos/sonos.py param1="--next" terminal=false refresh=true')
        print('update cache |color=green bash=/Users/skylartaylor/bitbar/sonos/sonos.py param1="--force" terminal=false refresh=true')
