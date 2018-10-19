# WireGuard Mesh Configurator

## 1.1.5 (October 19, 2018)

1. Patch for `avalon_framework` 1.6.0

## 1.1.4 (October 17, 2018)

1. Now using serialization to save profile instead of JSON.
1. Minor tweaks to the code for it to look more organized.

## Introduction

WireGuard mesh configurator is a tool that will help you generating peer configuration files for wireguard mesh networks. You generate configuration files for a large amount of peers easily and quickly via this tool.

## Gallery

![new_profile](https://user-images.githubusercontent.com/21986859/46922682-bb7aaf80-cfda-11e8-812e-b2458009302a.png)
*Creating a new mesh profile*

![save_load](https://user-images.githubusercontent.com/21986859/46922686-c9303500-cfda-11e8-9685-062a8a24ed27.png)
*Saving and Loading Profiles*

![generated_configs](https://user-images.githubusercontent.com/21986859/46964450-17464680-d076-11e8-9306-bfe69a88c858.png)
*Generated configuration files*

## Usages

### Installing WGC

Clone the repository and enter it.

```
$ git clone https://github.com/K4YT3X/wireguard-mesh-configurator.git
$ cd wireguard-mesh-configurator/
```

Run the tool.

```
$ python3 wireguard_mesh_configurator.py interactive
```

or

```
$ python3 wireguard_mesh_configurator.py int
```

### Creating a Profile

Run the `NewProfile` command to create a new profile.

```
[WGC]> NewProfile  # Create new profile
```

Then the peer enrolling wizard will ask you for all the information needed for all the peers. Select `n` when being asked if you want to add a new peer to end the wizard.

### Generating Configurations

Run the following command to dump your currently-loaded profile into configuration files and export them to `output path`.

```
[WGC]> GenerateConfigurations [output path]
```

### Viewing All Peers

To view all the peers configurations in the current profile:

```
[WGC]> ShowPeers
```

### Saving / Loading Profiles

To save a profile:

```
[WGC]> SaveProfile [output path]
```

To load a profile:

```
[WGC]> LoadProfile [output path]
```
