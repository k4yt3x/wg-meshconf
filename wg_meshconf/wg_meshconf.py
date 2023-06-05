#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: wg-meshconf
Creator: K4YT3X
Date Created: July 19, 2020
Last Modified: June 16, 2021

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2018-2021 K4YT3X
"""

import argparse
import pathlib
import sys

from .database_manager import DatabaseManager


def parse_arguments():
    """parse CLI arguments"""
    parser = argparse.ArgumentParser(
        prog="wg-meshconf", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-d",
        "--database",
        type=pathlib.Path,
        help="path where the database file is stored",
        default=pathlib.Path("database.csv"),
    )

    parser.add_argument(
        "--with-psk",
        help="generate PSKs for each connection",
        action="store_true"
    )

    # add subparsers for commands
    subparsers = parser.add_subparsers(dest="command")

    # initialize empty database
    subparsers.add_parser("init")

    # add new peer
    addpeer = subparsers.add_parser("addpeer")
    addpeer.add_argument("name", help="Name used to identify this node")
    addpeer.add_argument(
        "--address", help="address of the server", action="append", required=True
    )
    addpeer.add_argument("--endpoint", help="peer's public endpoint address")
    addpeer.add_argument(
        "--allowedips", help="additional allowed IP addresses", action="append"
    )
    addpeer.add_argument("--privatekey", help="private key of server interface")
    addpeer.add_argument("--presharedkeys", help="preshared keys for connection to other peers")
    addpeer.add_argument("--listenport", help="port to listen on", default=51820)
    addpeer.add_argument(
        "--persistentkeepalive", help="set persistent keepalive interval"
    )
    addpeer.add_argument("--fwmark", help="fwmark for outgoing packets")
    addpeer.add_argument("--dns", help="server interface DNS servers")
    addpeer.add_argument("--mtu", help="server interface MTU")
    addpeer.add_argument("--table", help="server routing table")
    addpeer.add_argument("--preup", help="command to run before interface is up")
    addpeer.add_argument("--postup", help="command to run after interface is up")
    addpeer.add_argument("--predown", help="command to run before interface is down")
    addpeer.add_argument("--postdown", help="command to run after interface is down")
    addpeer.add_argument(
        "--saveconfig",
        action="store_true",
        help="save server interface to config upon shutdown",
        default=None,
    )

    # update existing peer information
    updatepeer = subparsers.add_parser("updatepeer")
    updatepeer.add_argument("name", help="Name used to identify this node")
    updatepeer.add_argument("--address", help="address of the server", action="append")
    updatepeer.add_argument("--endpoint", help="peer's public endpoint address")
    updatepeer.add_argument(
        "--allowedips", help="additional allowed IP addresses", action="append"
    )
    updatepeer.add_argument("--privatekey", help="private key of server interface")
    updatepeer.add_argument("--presharedkeys", help="preshared keys for connection to other peers")
    updatepeer.add_argument("--listenport", help="port to listen on")
    updatepeer.add_argument(
        "--persistentkeepalive", help="set persistent keepalive interval"
    )
    updatepeer.add_argument("--fwmark", help="fwmark for outgoing packets")
    updatepeer.add_argument("--dns", help="server interface DNS servers")
    updatepeer.add_argument("--mtu", help="server interface MTU")
    updatepeer.add_argument("--table", help="server routing table")
    updatepeer.add_argument("--preup", help="command to run before interface is up")
    updatepeer.add_argument("--postup", help="command to run after interface is up")
    updatepeer.add_argument("--predown", help="command to run before interface is down")
    updatepeer.add_argument("--postdown", help="command to run after interface is down")
    updatepeer.add_argument(
        "--saveconfig",
        action="store_true",
        help="save server interface to config upon shutdown",
        default=None,
    )

    # delpeer deletes a peer form the database
    delpeer = subparsers.add_parser("delpeer")
    delpeer.add_argument("name", help="Name of peer to delete")

    # showpeers prints a table of all peers and their configurations
    showpeers = subparsers.add_parser("showpeers")
    showpeers.add_argument(
        "name",
        help="Name of the peer to query",
        nargs="?",
    )
    showpeers.add_argument(
        "-v",
        "--verbose",
        help="display all columns despite they hold empty values",
        action="store_true",
    )

    # generate config
    genconfig = subparsers.add_parser("genconfig")
    genconfig.add_argument(
        "name",
        help="Name of the peer to generate configuration for, \
            configuration for all peers are generated if omitted",
        nargs="?",
    )
    genconfig.add_argument(
        "-o",
        "--output",
        help="configuration file output directory",
        type=pathlib.Path,
        default=pathlib.Path.cwd() / "output",
    )

    return parser.parse_args()


# if the file is not being imported
def main():

    args = parse_arguments()

    database_manager = DatabaseManager(args.database)

    if args.command == "init":
        database_manager.init(args.with_psk)

    elif args.command == "addpeer":
        database_manager.addpeer(
            args.name,
            args.address,
            args.endpoint,
            args.allowedips,
            args.listenport,
            args.persistentkeepalive,
            args.fwmark,
            args.privatekey,
            args.presharedkeys,
            args.dns,
            args.mtu,
            args.table,
            args.preup,
            args.postup,
            args.predown,
            args.postdown,
            args.saveconfig,
        )

    elif args.command == "updatepeer":
        database_manager.updatepeer(
            args.name,
            args.address,
            args.endpoint,
            args.allowedips,
            args.listenport,
            args.persistentkeepalive,
            args.fwmark,
            args.privatekey,
            args.presharedkeys,
            args.dns,
            args.mtu,
            args.table,
            args.preup,
            args.postup,
            args.predown,
            args.postdown,
            args.saveconfig,
        )

    elif args.command == "delpeer":
        database_manager.delpeer(args.name)

    elif args.command == "showpeers":
        database_manager.showpeers(args.name, args.verbose)

    elif args.command == "genconfig":
        database_manager.genconfig(args.name, args.output, args.with_psk)

    # if no commands are specified
    else:
        print(
            "No command specified\nUse wg-meshconf --help to see available commands",
            file=sys.stderr,
        )
