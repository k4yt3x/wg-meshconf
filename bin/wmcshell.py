#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: WMC Interactive Shell
Dev: K4YT3X
Date Created: October 11, 2019
Last Modified: October 12, 2019
"""

# built-in imports
import cmd

# third-party imports
from avalon_framework import Avalon

# local imports
from profilemanager import ProfileManager
from wireguard import WireGuard


class WMCShell(cmd.Cmd):
    """ WireGuard Mesh Configurator Shell

    An interactive shell for WireGuard Mesh Configurator.
    """

    # define shell prompt
    prompt = f'{Avalon.FM.BD}[WMC]> {Avalon.FM.RST}'

    # define shell intro
    intro = 'Type ? to list all available commands.'

    # create global object for WireGuard handler
    wg = WireGuard()

    # create global object for profile manager
    pm = ProfileManager()

    def do_showpeers(self, arg):
        'show all peers in the current profile'
        for peer in self.pm.peers:
            peer.print_config()

    def do_jsonloadprofile(self, arg):
        'load profile from JSON file: jsonloadprofile PROFILE_PATH'
        self.pm.json_load_profile(arg)

    def do_jsonsaveprofile(self, arg):
        'save profile to JSON file: jsonsaveprofile PROFILE_PATH'
        self.pm.json_save_profile(arg)

    def do_pickleloadprofile(self, arg):
        'load profile from pickle file: pickleloadprofile PROFILE_PATH'
        self.pm.pickle_load_profile(arg)

    def do_picklesaveprofile(self, arg):
        'save profile to pickle file: picklesaveprofile PROFILE_PATH'
        self.pm.pickle_save_profile(arg)

    def do_newprofile(self, arg):
        'create new profile'
        self.pm.new_profile()

    def do_addpeer(self, arg):
        'add a new peer'
        self.pm.add_peer(self.wg)

    def do_deletepeer(self, arg):
        'delete a peer: deletepeer PEER_ADDRESS'
        self.pm.delete_peer(arg)

    def do_generateconfigs(self, arg):
        'generate configuration files: generateconfigs OUTPUT_PATH'
        self.pm.generate_configs(arg)

    def do_exit(self, arg):
        'exit the program'
        return True

    def do_quit(self, arg):
        'quit the program'
        return True
