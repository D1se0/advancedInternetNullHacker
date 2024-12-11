# Network Monitoring and Security Tools

This project contains two tools designed to monitor and protect your `local network`. One tool is based on monitoring **IP** addresses and the other on monitoring **MACs**. Both tools work with a list of allowed elements that are defined in specific text files (`.txt`).

## Prerequisites

Before running these tools, make sure you meet the following requirements:

- **Linux** (preferably based on `Debian`, such as `Kali Linux`).

- Tools installed:
  - `arp-scan`
  - `arpspoof`
  - `Python 3`

You can install `arp-scan` and `arpspoof` with the following command:

```bash
sudo apt-get install arp-scan dsniff
```

## Tools Included

### 1. IP Based Tool

### Description

This tool monitors active `IP` addresses on your `local network`. Detects any unknown `IP` address (not included in the allowed list) and performs `ARP Spoofing` to disconnect it from the network.

## Configuration

Create a file called `permitted_ip.txt` in the same directory as the script.
Add the allowed `IP` addresses, one per line.

### Execution

Run the `IP` based tool script with the following command:

```bash
python3 advanceInternetNullHacker_IP.py
```

During execution, you will need to enter the network interface (for example, `wlan0` or `eth0`).

### 2. MAC Based Tool

### Description

This tool monitors active `MAC` addresses on your local network. Detects any unknown `MAC` address (not included in the allowed list) and performs `ARP Spoofing` against the associated `IP`.

## Configuration

Create a file called `permitted_mac.txt` in the same directory as the script.
Add the allowed `MAC` addresses, one per line.

### Execution

Run the `MAC` based tool script with the following command:

```bash
python3 advanceInternetNullHacker_MAC.py
```

During execution, you will need to enter the network interface (for example, `wlan0` or `eth0`).

Active Device Identification: `knowARPHosts.sh`

The `knowARPHosts.sh` script allows you to identify the devices currently connected to your local network. Use `arp-scan` to get a list of active `IP` and `MAC` addresses.

## Use

Run the script with the following command:

```bash
bash knowARPHosts.sh
```

During execution, you will need to enter the network interface (for example, `wlan0` or `eth0`). This script will generate a list of connected devices in format:

```
192.168.1.1  c0:3c:04:3f:63:60  Manufacturer's Name
192.168.1.2  00:11:22:33:44:55  Manufacturer Name
```

Use this information to update the `permitted_ip.txt` and `permitted_mac.txt` files.

### Configuration Files

`permitted_ip.txt`: List of allowed `IP` addresses. Each address should go on a separate line.
`permitted_mac.txt`: List of allowed `MAC` addresses. Each address must go on a separate line.

Be sure to keep these lists up to date with the addresses of your known devices.

## Important Notes

Both tools run `ARP Spoofing` to disconnect unknown devices. This could be detected by more advanced network security systems.
Use these tools responsibly and only on 'networks that you manage'.
Run the scripts with administrator permissions (`sudo`) if you encounter permissions problems.

### Workflow Example

Run knowIP.sh to identify the current devices on your network.
Add the detected IP or MAC addresses to their respective files (`permitted_ip.txt` or `permitted_mac.txt`).
Run the corresponding tool (by `IP` or by `MAC`).
Monitor the status of connected devices and disconnect unknown ones automatically.

## Contact

If you have any questions or improvements for these tools, do not hesitate to share them. Enjoy a more secure network!

Creator: d1se0

Contact: ciberseguridad12345@gmail.com
