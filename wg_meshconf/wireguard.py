#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: WireGuard Python Bindings
Creator: K4YT3X
Date Created: October 11, 2019
Last Modified: July 19, 2020
"""

# built-in imports
import pathlib
import subprocess


class WireGuard:
    """WireGuard utility controller

    This class handles the interactions with the wg binary,
    including:

    - genkey
    - pubkey
    - genpsk
    """

    def __init__(self, wg_binary=pathlib.Path("/usr/bin/wg")):
        """
        Keyword Arguments:
            wg_binary {pathlib.Path} -- path of wg binary (default: {pathlib.Path("/usr/bin/wg")})

        Since the script might have to be run as root, it is bad practice to find wg using
        pathlib.Path(shutil.which("wg") since a malicious binary named wg can be under the current
        directory to intercept root privilege if SUID permission is given to the script.
        """
        self.wg_binary = wg_binary

    def genkey(self):
        """generate WG private key

        Generate a new wireguard private key via
        wg command.
        """
        return (
            subprocess.run(
                [str(self.wg_binary.absolute()), "genkey"],
                check=True,
                stdout=subprocess.PIPE,
            )
            .stdout.decode()
            .strip()
        )

    def pubkey(self, privkey: str) -> str:
        """convert WG private key into public key

        Uses wg pubkey command to convert the wg private
        key into a public key.

        Arguments:
            privkey {str} -- wg privkey

        Returns:
            str -- pubkey derived from privkey
        """
        return (
            subprocess.run(
                [str(self.wg_binary.absolute()), "pubkey"],
                check=True,
                stdout=subprocess.PIPE,
                input=privkey.encode("utf-8"),
            )
            .stdout.decode()
            .strip()
        )

    def genpsk(self):
        """generate a random base64 PSK"""
        return (
            subprocess.run(
                [str(self.wg_binary.absolute()), "genpsk"],
                check=True,
                stdout=subprocess.PIPE,
            )
            .stdout.decode()
            .strip()
        )
