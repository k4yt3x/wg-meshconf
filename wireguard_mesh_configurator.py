#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Wireguard Mesh Configurator
Dev: K4YT3X
Date Created: October 10, 2018
Last Modified: October 13, 2018

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2018 K4YT3X
"""
import argparse
import avalon_framework as avalon
import re
import readline
import subprocess
import traceback

VERSION = '1.0.1'

PEERS = []
CONFIG_OUTPUT = '/tmp/wireguard'


class Peer:
    """ Peer class

    Each object of this class represents a peer in
    the wireguard mesh network.
    """

    def __init__(self, address, private_key, keep_alive, listen_port, preshared_key=False):
        self.address = address
        self.private_key = private_key
        self.keep_alive = keep_alive
        self.listen_port = listen_port
        self.preshared_key = preshared_key


class WireGuard:
    """ WireGuard utility controller

    This class handles the interactions with the wg binary.
    """

    def __init__(self):
        pass

    def genkey(self):
        """ Generate WG private key

        Generate a new wireguard private key via
        wg command.
        """
        output = subprocess.Popen(['wg', 'genkey'], stdout=subprocess.PIPE).communicate()[0]
        return output.decode().replace('\n', '')

    def pubkey(self, public_key):
        """ Convert WG private key into public key

        Uses wg pubkey command to convert the wg private
        key into a public key.
        """
        process = subprocess.Popen(['wg', 'pubkey'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = process.communicate(input=public_key.encode('utf-8'))[0]
        return output.decode().replace('\n', '')

    def genpsk(self):
        """ Generate a random base64 psk
        """
        output = subprocess.Popen(['wg', 'genpsk'], stdout=subprocess.PIPE).communicate()[0]
        return output.decode().replace('\n', '')


def process_arguments():
    """This function parses all arguments
    """
    parser = argparse.ArgumentParser()
    control_group = parser.add_argument_group('Controls')
    control_group.add_argument('-v', "--verbose", help='Display debug output (TODO)', action="store_true", default=False)
    etc_group = parser.add_argument_group('Extra')
    etc_group.add_argument('-V', '--version', help='Display version and legal information and exit', action="store_true", default=False)
    return parser.parse_args()


def print_welcome():
    print('WireGuard Mesh Configurator {}'.format(VERSION))
    print('(C) 2018 K4YT3X')
    print('Licensed under GNU GPL v3')


def enroll_peer():
    """ Enroll a new peer
    """
    while True:
        address = avalon.gets('Address (leave empty if client only): ')
        result = re.match('^(?:\d{1,3}\.){3}\d{1,3}/{1}(?:\d\d?)?$', address)
        if result is None:
            avalon.error('Invalid address entered')
            avalon.error('Please use CIDR notation (e.g. 10.0.0.0/8)')
            continue
        break

    private_key = avalon.gets('Private key (leave empty for auto generation): ')
    if private_key == '':
        private_key = wg.genkey()
    keep_alive = avalon.ask('Keep alive?', False)
    listen_port = avalon.gets('Listen port (leave empty for client): ')
    """
    preshared_key = False
    if avalon.ask('Use a preshared key?', True):
        preshared_key = avalon.gets('Preshared Key (leave empty for auto generation): ')
        if preshared_key == '':
            preshared_key = wg.genpsk()
    peer = Peer(address, private_key, keep_alive, listen_port, preshared_key)
    """
    peer = Peer(address, private_key, keep_alive, listen_port)
    PEERS.append(peer)

    avalon.info('Peer information summary:')
    print('Address: {}'.format(peer.address))
    print('Private Key: {}'.format(peer.private_key))
    print('Keepalive: {}'.format(peer.keep_alive))
    print('Listen Port: {}'.format(peer.listen_port))
    # print('Preshared Key: {}'.format(peer.preshared_key))


def gen_configs():
    """ Generate configuration file for every peer

    This function reads the PEERS list, generates a
    configuration file for every peer, and export into
    the CONFIG_OUTPUT directory.
    """
    if len(PEERS) == 0:
        avalon.warning('No peers configured, exiting')
        exit(0)
    if len(PEERS) == 1:
        avalon.warning('Only one peer configured')

    avalon.info('Generating configuration files')

    for peer in PEERS:
        avalon.dbgInfo('Generating configuration file for {}'.format(peer.address))
        with open('{}/{}.conf'.format(CONFIG_OUTPUT, peer.address.split('/')[0]), 'w') as config:

            # Write Interface config
            config.write('[Interface]\n')
            config.write('PrivateKey = {}\n'.format(peer.private_key))
            if peer.address != '':
                config.write('Address = {}\n'.format(peer.address))
            if peer.listen_port != '':
                config.write('ListenPort = {}\n'.format(peer.listen_port))

            # Write peers' information
            for p in PEERS:
                if p.address == peer.address:
                    # Skip if peer is self
                    continue
                config.write('\n[Peer]\n')
                config.write('PublicKey = {}\n'.format(wg.pubkey(p.private_key)))
                config.write('AllowedIPs = {}\n'.format(p.address))
                if peer.keep_alive:
                    config.write('PersistentKeepalive = 25\n')
                if peer.preshared_key:
                    config.write('PresharedKey = {}\n'.format(p.preshared_key))


def get_peers_settings():
    """ Get all peers' settings

    Keep enrolling peers until the user aborts.
    """
    while avalon.ask('Add new peer?', True):
        enroll_peer()


if __name__ == '__main__':
    try:
        # Print welcome message
        print_welcome()

        # Parse command line arguments
        args = process_arguments()

        # Display version and legal information (--version)
        if args.version:  # prints program legal / dev / version info
            print("Current Version: " + VERSION)
            print("Author: K4YT3X")
            print("License: GNU GPL v3")
            print("Github Page: https://github.com/K4YT3X/wireguard-mesh-configurator")
            print("Contact: k4yt3x@k4yt3x.com\n")
            exit(0)

        # Create object for wireguard binary handler
        wg = WireGuard()

        # Start addding peers
        get_peers_settings()

        # Generate configuration files
        gen_configs()
    except KeyboardInterrupt:
        print()
        avalon.warning('Keyboard interruption caught, exiting')
        exit(1)
    except Exception:
        avalon.error('Exception caught')
        traceback.print_exc()
        exit(1)
