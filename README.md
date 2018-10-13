# WireGuard Mesh Configurator

## 1.0.1 (October 13, 2018)

1. Enhanced CLI
1. Added legal information

## Introduction

WireGuard mesh configurator is a tool that will help you generating peer configuration files for wireguard mesh networks. You generate configuration files for a large amount of peers easily and quickly via this tool.

## Gallery

![configurating](https://user-images.githubusercontent.com/21986859/46910822-4dba7f00-cf19-11e8-84c6-f354a7281925.png)
*Configuring a mesh network*

![generated_configs](https://user-images.githubusercontent.com/21986859/46910818-46937100-cf19-11e8-9ea3-965019293a5c.png)
*Generated configuration files*

## Usages

Clone the repository and enter it.

```
$ git clone https://github.com/K4YT3X/wireguard-mesh-configurator.git
$ cd wireguard-mesh-configurator/
```

Create a temporary folder for exporting configuration files.

```
$ mkdir /tmp/wireguard
```

Run the tool.

```
$ python3 wireguard_mesh_configurator.py
```

Then you will find all the generated configuration files under `/tmp/wireguard`.