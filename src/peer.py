#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: WireGuard Peer
Dev: K4YT3X
Date Created: October 11, 2019
Last Modified: October 12, 2019
"""

# third-party imports
from avalon_framework import Avalon


class Peer:
    """ Peer class

    Each object of this class represents a peer in
    the wireguard mesh network.
    """

    def __init__(self):
        pass
        """
        # mandatory fields
        self.private_key = private_key

        # optional fields
        for key in kwargs:
            self.__dict__.update(key, kwargs[key])

        self.private_key = private_key
        self.Address = address
        self.public_address = public_address
        self.listen_port = listen_port
        self.keep_alive = keep_alive
        self.preshared_key = kwargs.get('preshared_key')
        self.alias = kwargs.get('alias')
        self.description = kwargs.get('description')
        self.table = kwargs.get('table')
        self.postup = kwargs.get('postup')
        self.predown = kwargs.get('predown')
        """

    def print_config(peer):
        """ Print the configuration of a specific peer

        Input takes one Peer object.
        """
        if peer.__dict__.get('# Alias'):
            Avalon.info(f'{peer.__dict__["# Alias"]} information summary:')
        elif peer.__dict__.get('Address'):
            Avalon.info(f'{peer.Address} information summary:')

        for key in peer.__dict__:
            if isinstance(key, str) and key.startswith('#'):
                print(f'{key}: {peer.__dict__[key]}')

        for key in peer.__dict__:
            if peer.__dict__[key] != '' and peer.__dict__[key] is not None:
                if isinstance(key, str) and key.startswith('#'):
                    continue
                print(f'{key} = {peer.__dict__[key]}')
