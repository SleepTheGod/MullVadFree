# MullVadFree

MullVadFree is a Python script designed to automate the connection to a VPN using SOCKS5 proxies and relays from the Mullvad VPN service. This script fetches the proxy and relay data, generates an OpenVPN config dynamically, and establishes a VPN connection.

## Features

- Fetches SOCKS5 proxy data from Mullvad API
- Fetches relay information from Mullvad API
- Generates an OpenVPN config file dynamically based on proxy and relay data
- Automates the connection to the VPN using OpenVPN
- Automatically retries the connection every 30 seconds if it fails

## Requirements

- Python 3.x
- `requests` library
- OpenVPN installed on your system
- Valid certificates for OpenVPN (`ca.crt`, `client.crt`, and `client.key`)

### Install Dependencies

To install the required dependencies, use the following command:

```bash
pip install -r requirements.txt
```
# Endpoints
```
https://api.mullvad.net/www/relays/all/?action=query&titles=Alex&format=json&formatversion=2
https://api.mullvad.net/network/v1-beta1/socks-proxies
```
