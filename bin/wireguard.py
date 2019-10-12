#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: WireGuard Utility Controller
Dev: K4YT3X
Date Created: October 11, 2019
Last Modified: October 12, 2019
"""

# built-in imports
import pathlib
import shutil

# local imports
from utilities import Utilities


class WireGuard:
    """ WireGuard utility controller

    This class handles the interactions with the wg binary,
    including:

    - genkey
    - pubkey
    - genpsk
    """

    def __init__(self, wg_binary=pathlib.Path(shutil.which('wg'))):
        """
        Keyword Arguments:
            wg_binary {pathlib.Path} -- path of wg binary (default: {pathlib.Path(shutil.which('wg'))})
        """
        self.wg_binary = wg_binary

    def genkey(self):
        """ generate WG private key

        Generate a new wireguard private key via
        wg command.
        """
        return Utilities.execute([self.wg_binary, 'genkey'])

    def pubkey(self, private_key: str) -> str:
        """  convert WG private key into public key

        Uses wg pubkey command to convert the wg private
        key into a public key.

        Arguments:
            private_key {str} -- wg privkey

        Returns:
            str -- pubkey derived from privkey
        """
        return Utilities.execute([self.wg_binary, 'pubkey'], input_value=private_key.encode('utf-8'))

    def genpsk(self):
        """ generate a random base64 psk
        """
        return Utilities.execute([self.wg_binary, 'genpsk'])
