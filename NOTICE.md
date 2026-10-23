# Third-party code

`src/rrnet.s` sets up the CS8900a chip of the RR-Net cartridge the way the cs8900a driver of
[ip65](https://github.com/cc65/ip65) does. ip65 is distributed under the Mozilla Public License
1.1 (https://www.mozilla.org/MPL/1.1/).

The Ultimate Command Interface follows Gideon Zweijtzer's firmware
([1541ultimate](https://github.com/GideonZ/1541ultimate)); the command OPEN_UDP_LOCAL (`$0A`) is
JC-000's ([#1016](https://github.com/GideonZ/1541ultimate/pull/1016)).

The Commodore 64 Ultimate and the Commodore name belong to their owners. This is an independent
test program, not made or endorsed by Commodore.
