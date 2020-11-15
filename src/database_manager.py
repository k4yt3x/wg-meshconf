#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Database Manager
Dev: K4YT3X
Date Created: July 19, 2020
Last Modified: November 15, 2020
"""

# built-in imports
import copy
import json
import pathlib
import sys

# third party imports
from prettytable import PrettyTable

# local imports
from wireguard import WireGuard

INTERFACE_ATTRIBUTES = [
    "Address",
    "Endpoint",
    "PrivateKey",
    "ListenPort",
    "FwMark",
    "DNS",
    "MTU",
    "Table",
    "PreUp",
    "PostUp",
    "PreDown",
    "PostDown",
    "SaveConfig",
]

INTERFACE_OPTIONAL_ATTRIBUTES = [
    "Endpoint",
    "ListenPort",
    "FwMark",
    "DNS",
    "MTU",
    "Table",
    "PreUp",
    "PostUp",
    "PreDown",
    "PostDown",
    "SaveConfig",
]

PEER_ATTRIBUTES = [
    "PublicKey",
    "PresharedKey",
    "AllowedIPs",
    "Endpoint",
    "PersistentKeepalive",
]


class DatabaseManager:
    def __init__(self, database_path: pathlib.Path):
        self.database_path = database_path
        self.database_template = {"peers": {}}
        self.wireguard = WireGuard()

    def read_database(self):
        """ read database file into dict

        Returns:
            dict: content of database file in dict format
        """
        if not self.database_path.is_file():
            return self.database_template

        with self.database_path.open(mode="r", encoding="utf-8") as database_file:
            return json.load(database_file)

    def write_database(self, data: dict):
        """ dump data into database file

        Args:
            data (dict): content of database
        """
        with self.database_path.open(mode="w", encoding="utf-8") as database_file:
            json.dump(data, database_file, indent=4)

    def addpeer(
        self,
        name: str,
        Address: list,
        Endpoint: str = None,
        ListenPort: int = None,
        FwMark: str = None,
        PrivateKey: str = None,
        DNS: str = None,
        MTU: int = None,
        Table: str = None,
        PreUp: str = None,
        PostUp: str = None,
        PreDown: str = None,
        PostDown: str = None,
        SaveConfig: bool = None,
    ):
        database = copy.deepcopy(self.database_template)
        database.update(self.read_database())

        if name in database["peers"]:
            print(f"Peer with name {name} already exists")
            return

        database["peers"][name] = {}

        # if private key is not specified, generate one
        if locals().get("PrivateKey") is None:
            privatekey = self.wireguard.genkey()
            database["peers"][name]["PrivateKey"] = privatekey

        for key in INTERFACE_ATTRIBUTES:
            if locals().get(key) is not None:
                database["peers"][name][key] = locals().get(key)

        self.write_database(database)

    def updatepeer(
        self,
        name: str,
        Address: list = None,
        Endpoint: str = None,
        ListenPort: int = None,
        FwMark: str = None,
        PrivateKey: str = None,
        DNS: str = None,
        MTU: int = None,
        Table: str = None,
        PreUp: str = None,
        PostUp: str = None,
        PreDown: str = None,
        PostDown: str = None,
        SaveConfig: bool = None,
    ):
        database = copy.deepcopy(self.database_template)
        database.update(self.read_database())

        if name not in database["peers"]:
            print(f"Peer with name {name} does not exist")
            return

        for key in INTERFACE_ATTRIBUTES:
            if locals().get(key) is not None:
                database["peers"][name][key] = locals().get(key)

        self.write_database(database)

    def delpeer(self, name: str):
        database = copy.deepcopy(self.database_template)
        database.update(self.read_database())

        # abort if user doesn't exist
        if name not in database["peers"]:
            print(f"Peer with ID {name} does not exist")
            return

        database["peers"].pop(name, None)

        # write changes into database
        self.write_database(database)

    def showpeers(self, style: str = "table", simplify: bool = False):
        database = self.read_database()

        if style == "table":
            table = PrettyTable()
            field_names = ["name"]

            if simplify is True:
                for name in database["peers"]:
                    for key in INTERFACE_ATTRIBUTES:
                        if (
                            database["peers"][name].get(key) is not None
                            and key not in field_names
                        ):
                            field_names.append(key)
            else:
                field_names += INTERFACE_ATTRIBUTES

            table.field_names = field_names

            for name in database["peers"]:
                table.add_row(
                    [name]
                    + [
                        database["peers"][name].get(k)
                        if not isinstance(database["peers"][name].get(k), list)
                        else ",".join(database["peers"][name].get(k))
                        for k in [i for i in table.field_names if i != "name"]
                    ]
                )

            print(table)

        elif style == "text":
            for name in database["peers"]:
                print(f"{'peer': <14}{name}")
                for key in INTERFACE_ATTRIBUTES:
                    print(f"{key: <14}{database['peers'][name].get(key)}")
                print()

    def genconfig(self, name: str, output: pathlib.Path):
        database = self.read_database()

        # check if peer ID is specified
        if name is not None:
            peers = [name]
        else:
            peers = [p for p in database["peers"]]

        # check if output directory is valid
        # create output directory if it does not exist
        if output.exists() and not output.is_dir():
            print("Error: output path already exists and is not a directory", file=sys.stderr)
            raise FileExistsError
        elif not output.exists():
            print(f"Creating output directory: {output}")
            output.mkdir(exist_ok=True)

        # for every peer in the database
        for peer in peers:
            with (output / f"{peer}.conf").open('w') as config:
                config.write("[Interface]\n")
                config.write("# Name: {}\n".format(peer))
                config.write("Address = {}\n".format(", ".join(database["peers"][peer]["Address"])))
                config.write("PrivateKey = {}\n".format(database["peers"][peer]["PrivateKey"]))

                for key in INTERFACE_OPTIONAL_ATTRIBUTES:
                    if database["peers"][peer].get(key) is not None:
                        config.write("{} = {}\n".format(key, database["peers"][peer][key]))

                # generate [Peer] sections for all other peers
                for p in [i for i in database["peers"] if i != peer]:
                    config.write("\n[Peer]\n")
                    config.write("# Name: {}\n".format(p))
                    config.write(
                        "PublicKey = {}\n".format(
                            self.wireguard.pubkey(database["peers"][p]["PrivateKey"])
                        )
                    )

                    if database["peers"][p].get("Endpoint") is not None:
                        config.write("Endpoint = {}\n".format(database["peers"][p]["Endpoint"]))

                    if database["peers"][p].get("Address") is not None:
                        config.write(
                            "AllowedIPs = {}\n".format(
                                ", ".join(database["peers"][p]["Address"])
                            )
                        )
