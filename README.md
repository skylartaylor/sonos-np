sonos-np
========

Now Playing Script for Sonos Systems with options for control.

Originally developed for use with [bitbar for macOS](https://github.com/matryer/bitbar).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to interact with Sonos, you'll need to install [SoCo](https://github.com/SoCo/SoCo) (tested with 0.12).

```
pip install --user soco==0.12
```

### Usage
From the command line, sonos.py can be executed with a number of flags:

| Flag              | Description                                                         |
|-------------------|---------------------------------------------------------------------|
| --play            | Play Currently Paused Media                                         |
| --pause           | Pause Currently Paused Media                                        |
| --next            | Go Forward In The Queue                                             |
| --previous        | Go Backward In The Queue                                            |
| --set "Room Name" | Set Default Speaker to Named Speaker                                |
| --list            | List Sonos Speakers (Excluding Surround and Stereo Paired Speakers) |
| --force           | Forces Discovery of Sonos Network (useful when debugging)           |

like so:
```
./sonos.py --set "Living Room"
```

To use this plugin with [bitbar](https://github.com/matryer/bitbar) you'll need to do the following:

 1. Clone repository from Github
 2. Create shell script in your bitbar scripts folder pointing to sonos.py:
 ```
 #!/bin/bash
 PYTHONIOENCODING=utf-8 ~/path/to/repository/sonos.py "$@"
 ```
 3. Refresh bitbar, allowing time for Sonos discovery (10-15s on first start)
 4. Select sonos from menu bar, and select your current room

## Acknowledgments

* Thanks to Justin, your development abilities enable my desktop to look great
* [Developers of Soco](https://github.com/SoCo/SoCo/blob/master/AUTHORS.rst)
