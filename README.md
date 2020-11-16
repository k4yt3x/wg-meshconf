# WireGuard Mesh Configurator

## On the Horizon: `wg-dynamic`

`wg-dynamic` is a tool designed officially by the WireGuard developing team. This new utility will provide a convenient way of configuring networks dynamically, where mesh network being one of the them. If you're interested, check it out at [wg-dynamic@github](https://github.com/WireGuard/wg-dynamic) or [wg-dynamic@official repository](https://git.zx2c4.com/wg-dynamic).

## Introduction

wg-meshconf is a tool that will help you to generate peer configuration files for WireGuard mesh networks. You can easily and quickly create WireGuard mesh networks using this tool.

## Prerequisites

- Python 3

You used to have to install a bunch of other Python packages, but I cut them all off in version 2.0.0 to keep this software lightweight.

## Learn by an Example

Usages are dull and boring. Let's see a real-life example of how this tool can be used. This section will demonstrate how to create a simple mesh network with four nodes using wg-meshconf.

For this example, suppose you have four servers as shown below. These servers can reach each other via the `Endpoint` address. For instance, server `tokyo1` can ping server `shanghai1` with the address `shanghai1.com`.

![image](https://user-images.githubusercontent.com/21986859/99200153-94839e80-279b-11eb-81c9-189b609661ee.png)

### Step 1: Add Peers

First we need to add all peers in the mesh network into the database. The basic syntax for adding new peers is:

```shell
./wg-meshconf addpeer NAME --address IP_ADDRESS --address IP_ADDRESS_2 --endpoint ENDPOINT
```

- New private key will be generated automatically if unspecified
- ListenPort defaults to 51820 per WireGuard standard
- All other values are left empty by default

There are more options which you can specify. Use the command `./wg-meshconf addpeer -h` for more details.

After adding all the peers into the database, you can verify that they have all been added correctly via the `./wg-meshconf showpeers` command. The `simplify` switch here omits all columns with only `None`s.

![image](https://user-images.githubusercontent.com/21986859/99202459-1dec9e00-27a7-11eb-8190-a5a3c6644d2a.png)

### Step 2: Export Configuration Files

Use the `genconfig` command to generate configuration files for all peers. You may also export configurations for only one peer by specifying the peer's name.

The configuration files will be named after the peers' names. By default, all configuration files are exported into a subdirectory named `output`. You can change this by specifying output directory using the `-o` or the `--output` option.

![image](https://user-images.githubusercontent.com/21986859/99202483-352b8b80-27a7-11eb-8479-8749e945a81d.png)

### Step 3: Copy Configuration Files to Peers

Copy each of the configuration files to the corresponding peers.

![image](https://user-images.githubusercontent.com/21986859/99201225-e4fdfa80-27a1-11eb-9b27-6e684d30b784.png)

### Step 4: Start WireGuard Services

Start up the WireGuard interfaces using the `wg-quick` command. It is also possible to control WireGuard interfaces via WireGuard's `wg-quick@` systemd service. WireGuard status can be verified via the `wg` command after WireGuard interfaces are set up.

![image](https://user-images.githubusercontent.com/21986859/99202554-7459dc80-27a7-11eb-9e92-44cd02bdc2f7.png)

### Step 5: Verify Connectivity

Verify that all endpoints have been configured properly and can connect to each other.

![image](https://user-images.githubusercontent.com/21986859/99202822-5e98e700-27a8-11eb-8bb2-3e0d2222258f.png)

Done. Now a mesh network has been created between the four servers.

## Updating Peer Information

If you would like to update a peer's information, use the `updatepeer` command. The syntax of `updatepeer` is the same as that of the `addpeer` command. Instead of adding a new peer, this command overwrites values in existing entries.

In the example below, suppose you would like to update `tokyo1`'s endpoint address and change it to `tokyo321.com`. Use the `updatepeer` command and specify the new endpoint to be `tokyo321.com`. This will overwrite `tokyo1`'s existing `Endpoint` value.

![image](https://user-images.githubusercontent.com/21986859/99204025-3a3f0980-27ac-11eb-9159-0e40fc2eefeb.png)

## Deleting Peers

Use the `delpeer` command to delete peers. The syntax is `delpeer PEER_NAME`.

This example below shows how to delete the peer `tokyo1` from the database.

![image](https://user-images.githubusercontent.com/21986859/99204215-e123a580-27ac-11eb-93b1-d07345004fab.png)

## Database Files

Unlike 1.x.x versions of wg-meshconf, version 2.0.0 does not require the user to save or load profiles. Instead, all add peer, update peer and delete peer operations are file operations. The changes will be saved to the database file immediately. The database file to use can be specified via the `-d` or the `--database` option. If no database file is specified, `database.json` will be used.

Database files are essentially just JSON files. Below is an example.

```json
{
    "peers": {
        "tokyo1": {
            "PrivateKey": "8NgwtCjISH6tznAzj5e3ujr3llxgdrLzCje9U6mUD1c=",
            "Address": [
                "10.1.0.1/16"
            ],
            "ListenPort": 51820,
            "Endpoint": "tokyo1.com"
        },
        "germany1": {
            "PrivateKey": "GFtKAG0zhWfa3LxPOG/d9zN6OfZKjL1CTyZih4oUjlU=",
            "Address": [
                "10.2.0.1/16"
            ],
            "ListenPort": 51820,
            "Endpoint": "germany1.com"
        }
    }
}
```

## Detailed Usages

You may refer to the program's help page for usages. Use the `-h` switch or the `--help` switch to print the help page.

```shell
$./wg-meshconf -h
usage: wg-meshconf [-h] [-d DATABASE] {addpeer,updatepeer,delpeer,showpeers,genconfig} ...

positional arguments:
  {addpeer,updatepeer,delpeer,showpeers,genconfig}

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        path where the database file is stored (default: database.json)
```

Specify `-h` or `--help` after a command to see this command's usages.

```shell
$./wg-meshconf addpeer -h
usage: wg-meshconf addpeer [-h] --address ADDRESS [--endpoint ENDPOINT] [--privatekey PRIVATEKEY] [--listenport LISTENPORT] [--fwmark FWMARK] [--dns DNS] [--mtu MTU] [--table TABLE] [--preup PREUP] [--postup POSTUP] [--predown PREDOWN] [--postdown POSTDOWN] [--saveconfig] name

positional arguments:
  name                  Name used to identify this node

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS     address of the server
  --endpoint ENDPOINT   peer's public endpoint address
  --privatekey PRIVATEKEY
                        private key of server interface
  --listenport LISTENPORT
                        port to listen on
  --fwmark FWMARK       fwmark for outgoing packets
  --dns DNS             server interface DNS servers
  --mtu MTU             server interface MTU
  --table TABLE         server routing table
  --preup PREUP         command to run before interface is up
  --postup POSTUP       command to run after interface is up
  --predown PREDOWN     command to run before interface is down
  --postdown POSTDOWN   command to run after interface is down
  --saveconfig          save server interface to config upon shutdown
```
