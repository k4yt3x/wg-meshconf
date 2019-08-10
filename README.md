# WireGuard Mesh Configurator

## On the Horizon: `wg-dynamic`

`wg-dynamic` is a tool designed officially by WireGuard developing team. This new utility will provide a convenient way of configuring networks dynamically, where mesh network being one of the them. If you're interested, check it out at [wg-dynamic@github](https://github.com/WireGuard/wg-dynamic) or [wg-dynamic@official repository](https://git.zx2c4.com/wg-dynamic)).

## 1.3.0 (August 10, 2019)

- Changed Peer object read and write method
  - Now using `peer.__dict__` instead of receiving values in object constructor
- Added new wg-quick fields
  - Table
  - PreUp
  - PostUp
  - PreDown
  - PostDown
- Peer configuration now separated into basic and advanced configurations

## 1.2.0 (May 16, 2019)

- You can now set Aliases and Descriptions for peers.
- Profiles can now be saved and loaded in JSON format.

## 1.1.7 (Feburary 20, 2019)

- Public address can now be either FQDN or IP address, as requested by @KipourosV

## Introduction

WireGuard mesh configurator is a tool that will help you generating peer configuration files for wireguard mesh networks. You generate configuration files for a large amount of peers easily and quickly via this tool.

## Prerequisites

### System Packages

|Package|Explanation|Example|
|-|-|-|
|ncurses dev package|Required by the installation of the Python `readline` library.|`libncurses5-dev` on Debian|

### Python Libraries

The following libraries can be installed easily through executing `pip3 install -r requirements.txt` under the root directory of this repository.

|Package|Explanation|
|-|-|
|`avalon_framework`|Command line I/O library|
|`readline`|For better interactive command line interface|
|`netaddr`|For calculating IP addresses|

## Learn By An Example

In this section, we will be going through how to configure a mesh network with the topology shown below using wireguard mesh configurator (this tool, **WGC**).

![example_topology](https://user-images.githubusercontent.com/21986859/47622988-edfbd080-dae1-11e8-97f6-ff8ef56ffecc.png)

### Step 1: Create a Profile

Launch the WGC interactive shell. This will be where you give instructions to WGC.

```
$ python3 wireguard_mesh_configurator.py int
```

Every profile in WGC contains a complete topology. To create a new mesh network, we start by creating a new profile. Once a profile is created, you will be prompted automatically to enroll new peers. This leads us to the next step.

```
[WGC]> new
```

![step1](https://user-images.githubusercontent.com/21986859/47623179-5d72bf80-dae4-11e8-9705-9158ea8f75c2.png)

### Step 2: Enroll Peers

Now that a profile has already been created, we need to input peers' information into WGC, so it knows the layout of the network.

![enroll_peers](https://user-images.githubusercontent.com/21986859/47623237-526c5f00-dae5-11e8-823a-863e5372faa9.png)

### Step 3: Export Configurations

Now that we have all the peers in the profile, it's time to export everything into wireguard configuration files. We can dump configuration files into a directory using the `GenerateConfigurations` command. The following command will dump all the configuration files into the `/tmp/wg` directory.

```
[WGC]> gen /tmp/wg
```

![gen_config](https://user-images.githubusercontent.com/21986859/47623276-f8b86480-dae5-11e8-9c41-54bab4523031.png)

We can also take a look at the generated configuration files.

![generated_configs](https://user-images.githubusercontent.com/21986859/47623330-a3c91e00-dae6-11e8-84bd-85971b3092b3.png)

### Step 4: Copy Configuration Files to Endpoints

With the configuration files generated, all that's left to do is to copy the configuration files to the endpoints. Copy each configuration to the corresponding device with any method you like (sftp, ftps, plain copy & paste, etc.).

Put the configuration file to `/etc/wireguard/wg0.conf` is recommended, since it will make us able to use the `wg-quick` command for express configuration.

### Step 5: Enable WireGuard and Apply the Configuration

Lets tell wireguard to create an interface with this configuration and make it a service, so the interface will be created as system is booted up.

```
$ sudo wg-quick up wg0
$ sudo systemctl enable wg-quick@wg0
```

![apply_enable](https://user-images.githubusercontent.com/21986859/47623379-3f5a8e80-dae7-11e8-9350-555e61884691.png)

You can then verify the wireguard status via the `wg` command.

```
$ sudo wg
```

![wg_status](https://user-images.githubusercontent.com/21986859/47623489-9ca30f80-dae8-11e8-9241-3c7421b982db.png)

### Step 6: Saving and Loading Profiles

We can save a profile for future use using the `SaveProfile` command. The following example will save the profile to `/home/k4yt3x/example.pkl`.

```
[WGC]> save /home/k4yt3x/example.pkl
```

To load the profile, just use the `LoadProfile` command.

```
[WGC]> load /home/k4yt3x/example.pkl
```

Then you can use `ShowPeers` command to verify that everything has been loaded correctly.

```
[WGC]> sh
```

![saving_loading](https://user-images.githubusercontent.com/21986859/47623453-2d2d2000-dae8-11e8-9c21-528a7d9acde0.png)

That concludes the "Learn By An Example" section. Hope it helps.

## Detailed Usages

### Installing WGC

Clone the repository and enter it.

```
$ git clone https://github.com/K4YT3X/wireguard-mesh-configurator.git
$ cd wireguard-mesh-configurator/
```

Install Python 3 dependencies.

```
$ sudo pip3 install -r requirements.txt
```

Run the tool.

```
$ python3 wireguard_mesh_configurator.py interactive
```

or

```
$ python3 wireguard_mesh_configurator.py int
```

### Creating A Profile

Run the `NewProfile` command to create a new profile.

```
[WGC]> NewProfile  # Create new profile
```

Then the peer enrolling wizard will ask you for all the information needed for all the peers. Select `n` when being asked if you want to add a new peer to end the wizard.

### Adding a Peer

Use the `AddPeer` command to initialize the wizard of appending a new peer to the profile.

```
[WGC]> AddPeer
```

### Deleting a Peer

Use the `DeletePeer` command to remove a peer from the profile.

```
[WGC]> DeletePeer [Peer Address (e.g. 10.0.0.1/8)]
```

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

To save a profile in JSON format:

```
[WGC]> JSONSaveProfile [output path]
```

To save a profile in Pickle format:

```
[WGC]> PickleSaveProfile [output path]
```

To load a profile in JSON format:

```
[WGC]> JSONLoadProfile [output path]
```

To load a profile in Pickle format:

```
[WGC]> PickleLoadProfile [output path]
```
