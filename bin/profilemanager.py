#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: WireGuard Profile Manager
Dev: K4YT3X
Date Created: October 11, 2019
Last Modified: October 12, 2019
"""

# built-in imports
import contextlib
import json
import os
import pathlib
import pickle
import re

# third-party imports
from avalon_framework import Avalon
import netaddr

# local imports
from peer import Peer
from wireguard import WireGuard


# attributes that should be written into the
# [Interface] section of the configuration file
LOCAL_ATTRIBUTES = [
    'Address',
    'PrivateKey',
    'ListenPort',
    'DNS',
    'MTU',
    'Table',
    'PreUp',
    'PostUp',
    'PreDown',
    'PostDown',
    'SaveConfig'
]

# attributes that should be written into the
# [Peer] section of the configuration file
PEER_ATTRIBUTES = [
    'PublicKey',
    'AllowedIPs',
    # 'Endpoint',
    'PersistentKeepalive',
    'PresharedKey'
]


class ProfileManager(object):
    """ Profile manager

    Each instance of this class represents a profile,
    which is a complete topology of a mesh / c/s network.
    """

    def __init__(self):
        """ Initialize peers list
        """
        self.peers = []

    def pickle_load_profile(self, profile_path: pathlib.Path):
        """ load profile from a file

        open the pickle file, de-serialize the content and
        load it back into the profile manager

        Arguments:
            profile_path {pathlib.Path} -- path of profile to load
        """
        self.peers = []
        Avalon.debug_info(f'Loading profile from: {profile_path}')
        with open(profile_path, 'rb') as profile:
            self.peers = pickle.load(profile)

    def pickle_save_profile(self, profile_path: pathlib.Path):
        """ save current profile to a file

        serializes the current profile with pickle
        and dumps it into a file

        Arguments:
            profile_path {pathlib.Path} -- path to save profile to

        Returns:
            number -- 1 if failed
        """

        # If profile already exists (file or link), ask the user if
        # we should overwrite it.
        if os.path.isfile(profile_path) or os.path.islink(profile_path):
            if not Avalon.ask('File already exists. Overwrite?', True):
                Avalon.warning('Aborted saving profile')
                return 1

        # Abort if profile_path points to a directory
        if os.path.isdir(profile_path):
            Avalon.warning('Destination path is a directory')
            Avalon.warning('Aborted saving profile')
            return 1

        # Finally, write the profile into the destination file
        Avalon.debug_info(f'Writing profile to: {profile_path}')
        with open(profile_path, 'wb') as profile:
            pickle.dump(self.peers, profile)
            profile.close()

    def json_load_profile(self, profile_path: pathlib.Path):
        """ load profile to JSON file

        dumps each peer's __dict__ to JSON file

        Arguments:
            profile_path {pathlib.Path} -- path of profile to load
        """
        self.peers = []
        Avalon.debug_info(f'Loading profile from: {profile_path}')
        with open(profile_path, 'rb') as profile:
            loaded_profiles = json.load(profile)

        for p in loaded_profiles['peers']:
            peer = Peer()
            peer.__dict__.update(p)
            self.peers.append(peer)

    def json_save_profile(self, profile_path: pathlib.Path):
        """ save current profile to a JSON file

        Arguments:
            profile_path {pathlib.Path} -- path to save profile to

        Returns:
            number -- 1 if failed
        """

        # convert profile_path into pathlib.Path object
        profile_path = pathlib.Path(profile_path)

        # abort if profile_path points to a directory
        if profile_path.is_dir():
            Avalon.warning('Destination path is a directory')
            Avalon.warning('Aborted saving profile')
            return 1

        # if profile already exists (file or link)
        # ask the user if we should overwrite it
        if profile_path.exists():
            if not Avalon.ask('File already exists. Overwrite?', True):
                Avalon.warning('Aborted saving profile')
                return 1

        # finally, write the profile into the destination file
        Avalon.debug_info(f'Writing profile to: {profile_path}')

        peers_dict = {}
        peers_dict['peers'] = []

        for peer in self.peers:
            peers_dict['peers'].append(peer.__dict__)

        with open(profile_path, 'w') as profile:
            json.dump(peers_dict, profile, indent=4)
            profile.close()

    def new_profile(self):
        """ create new profile and flush the peers list
        """

        # Warn the user before flushing configurations
        if len(self.peers) != 0:
            Avalon.warning('This will flush the currently loaded profile!')
            if not Avalon.ask('Continue?', False):
                return

        # Reset self.peers and start enrolling new peer data
        self.peers = []

    def add_peer(self, wg: WireGuard):
        """ enroll a new peer

        Gets all the information needed to generate a
        new Peer class object.

        Arguments:
            wg {WireGuard} -- wireguard utility object
        """

        # initialize empty dict for peer configuration
        peer_config = {}

        # Get peer private key
        while True:
            peer_config['PrivateKey'] = Avalon.gets('Private key (leave empty for auto generation): ', default=wg.genkey())

            # generate public key from private key
            peer_config['PublicKey'] = wg.pubkey(peer_config['PrivateKey'])

            # if there's no pubkey generated, input is invalid
            if peer_config['PublicKey'] != '':
                break

            Avalon.error('Invalid private key format')

        # Get peer tunnel address
        while True:
            address = Avalon.gets('Address (leave empty if client only) [IP/CIDR]: ')
            try:
                peer_config['Address'] = address = str(netaddr.IPNetwork(address))
            except netaddr.core.AddrFormatError:
                Avalon.error('Invalid address entered')
                Avalon.error('Please use CIDR notation (e.g. 10.0.0.0/8)')
                continue
            break

        # Get peer public IP address
        while True:
            public_address = Avalon.gets('Public address (leave empty if client only) [IP|FQDN]: ')

            # check if public_address is valid IP or FQDN
            valid_address = False

            # check if input is valid IPv4/IPv6 address
            with contextlib.suppress(netaddr.core.AddrFormatError):
                netaddr.IPAddress(public_address)
                valid_address = True

            # check if input is valid FQDN
            if re.match('(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', public_address) is not None:
                valid_address = True

            if not valid_address and public_address != '':  # field not required
                Avalon.error('Invalid public address address entered')
                Avalon.error('Please enter an IP address or FQDN')
                continue
            break
        peer_config['Endpoint'] = public_address

        # Get peer listening port
        peer_config['ListenPort'] = Avalon.gets('Listen port (leave empty for client) [1-65535]: ')

        # Ask if this peer needs to be actively connected
        # if peer is behind NAT and needs to be accessed actively
        # PersistentKeepalive must be turned on (!= 0)
        peer_config['PersistentKeepalive'] = Avalon.ask('Keep alive?', False)

        # Get peer alias
        peer_config['# Alias'] = Avalon.gets('Alias (optional): ')

        # Get peer description
        peer_config['# Description'] = Avalon.gets('Description (optional): ')

        # start advanced configurations
        if Avalon.ask('Enter advanced configurations?'):

            # get peer table
            peer_config['AllowedIPs'] = Avalon.gets('AllowedIPs (optional): ')

            # get peer table
            peer_config['Table'] = Avalon.gets('Table (optional): ')

            # get peer preup
            peer_config['PreUp'] = Avalon.gets('PreUp (optional): ')

            # get peer postup
            peer_config['PostUp'] = Avalon.gets('PostUp (optional): ')

            # get peer predown
            peer_config['PreDown'] = Avalon.gets('PreDown (optional): ')

            # get peer predown
            peer_config['PostDown'] = Avalon.gets('PostDown (optional): ')

        # Create peer and append peer into the peers list
        peer = Peer()
        peer.__dict__.update(peer_config)

        self.peers.append(peer)
        peer.print_config()

    def delete_peer(self, address: str):
        """ delete a peer

        Delete a specific peer from the peer list.

        Arguments:
            address {str} -- address of peer
        """
        for peer in self.peers:
            if peer.Address == address:
                self.peers.remove(peer)

    def generate_configs(self, output_path: pathlib.Path):
        """ generate configuration file for every peer

        This function reads the PEERS list, generates a
        configuration file for every peer, and export into
        the CONFIG_OUTPUT directory.

        Arguments:
            output_path {pathlib.Path} -- path to store output configs

        Returns:
            number -- not 0 if failed
        """

        # convert output_path into pathlib.Path object
        output_path = pathlib.Path(output_path)

        if len(self.peers) == 0:
            Avalon.warning('No peers configured, exiting')
            exit(0)
        if len(self.peers) == 1:
            Avalon.warning('Only one peer configured')

        Avalon.info('Generating configuration files')

        # Abort is destination is a file / link
        if output_path.is_file() or output_path.is_symlink():
            Avalon.warning('Destination path is a file / link')
            Avalon.warning('Aborting configuration generation')
            return 1

        # Ask if user wants to create the output directory if it doesn't exist
        if not output_path.is_dir():
            if Avalon.ask('Output directory doesn\'t exist. Create output directory?', True):
                output_path.mkdir(parents=True, exist_ok=True)
            else:
                Avalon.warning('Aborting configuration generation')
                return 1

        # iterate through all peers and generate configuration for each peer
        for peer in self.peers:
            Avalon.debug_info(f'Generating configuration file for {peer.Address}')
            with open(output_path / f'{peer.Address.split("/")[0]}.conf', 'w') as config:

                # write Interface configuration
                config.write('[Interface]\n')

                # write all comment keys
                for key in peer.__dict__:

                    # if value is non-standard comment
                    if key.startswith('#'):
                        config.write(f'{key}: {peer.__dict__[key]}\n')

                # write all keys and values
                for key in [p for p in peer.__dict__ if p in LOCAL_ATTRIBUTES]:

                    # if value is not empty string or None
                    if peer.__dict__[key] != '' and peer.__dict__[key] is not None:
                        if key.startswith('#'):
                            continue
                        config.write(f'{key} = {peer.__dict__[key]}\n')

                # Write peers' information
                for p in self.peers:
                    if p.Address == peer.Address:
                        # Skip if peer is self
                        continue

                    config.write('\n[Peer]\n')

                    for k in p.__dict__:
                        if k.startswith('#'):
                            config.write(f'{k}: {p.__dict__[k]}\n')

                    # write endpoint information separately
                    # since it has a different format
                    config.write(f'Endpoint = {p.__dict__["public_address"]}:{p.__dict__["listen_port"]}\n')

                    # if value is not empty string or None
                    for k in [p for p in p.__dict__ if p in PEER_ATTRIBUTES]:
                        if p.__dict__[k] != '' and p.__dict__[k] is not None:
                            if k.startswith('#'):
                                continue
                            config.write(f'{k} = {p.__dict__[k]}\n')
