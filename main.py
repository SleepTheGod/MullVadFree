import requests
import subprocess
import time
import random
import os

# Fetch SOCKS5 proxies from Mullvad API
def get_proxies():
    url = "https://api.mullvad.net/network/v1-beta1/socks-proxies"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching proxy data.")
        return []
    
    try:
        data = response.json()
        if isinstance(data, list):
            print(f"Fetched proxies: {data}")  # Debug output
            return data
        else:
            print("Unexpected proxy response format.")
            return []
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return []

# Fetch relay information from Mullvad API
def get_relays():
    url = "https://api.mullvad.net/www/relays/all/?action=query&titles=Alex&format=json&formatversion=2"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching relay data.")
        return []
    
    try:
        data = response.json()
        if isinstance(data, dict):
            pages = data.get('query', {}).get('pages', {})
            print(f"Fetched relays: {pages}")  # Debug output
            return list(pages.values())  # Ensure we're getting the relays properly
        else:
            print("Unexpected response format.")
            return []
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return []

# Generate the OpenVPN config dynamically based on the selected proxy and relay
def generate_openvpn_config(proxy, relay):
    config_template = """
client
dev tun
proto udp
remote {proxy_ip} {proxy_port}
resolv-retry infinite
nobind
persist-key
persist-tun
auth-nocache
tls-client
<ca>
-----BEGIN CERTIFICATE-----
# Insert CA Certificate here
-----END CERTIFICATE-----
</ca>
<cert>
-----BEGIN CERTIFICATE-----
# Insert Client Certificate here
-----END CERTIFICATE-----
</cert>
<key>
-----BEGIN PRIVATE KEY-----
# Insert Private Key here
-----END PRIVATE KEY-----
</key>
# Adjust this with real relay info or other VPN-related settings
"""
    config_content = config_template.format(proxy_ip=proxy['ipv4_address'], proxy_port=proxy['port'])

    config_path = "/tmp/openvpn_config.ovpn"
    with open(config_path, "w") as config_file:
        config_file.write(config_content)
    return config_path

# Set up the VPN client using the fetched proxy and relay data
def setup_vpn(proxy, relay):
    print(f"Connecting to VPN using proxy {proxy['ipv4_address']}:{proxy['port']}...")
    config_path = generate_openvpn_config(proxy, relay)
    
    # Example VPN setup with OpenVPN
    command = [
        "openvpn",
        "--config", config_path,
        "--tls-client", "--auth-nocache",
        "--dev", "tun"
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("VPN connection established successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting VPN client: {e}")
        print(f"Error output: {e.stderr.decode()}")
    except FileNotFoundError as e:
        print(f"OpenVPN executable not found: {e}")

# Main function to run the VPN client with proxies and relays
def run_vpn_client():
    proxies = get_proxies()
    relays = get_relays()
    
    if not proxies or not relays:
        print("No proxies or relays found.")
        return

    # Randomly choose a proxy and relay (you can customize this logic)
    proxy = random.choice(proxies)
    relay = random.choice(relays)

    print(f"Using proxy: {proxy['hostname']}, {proxy['ipv4_address']}, Port: {proxy['port']}")
    print(f"Using relay: {relay.get('title', 'Unknown')}")

    # Set up VPN connection
    setup_vpn(proxy, relay)

# Automate the VPN client connection and retry
def automate_vpn_connection():
    while True:
        try:
            run_vpn_client()
            print("VPN session complete. Reconnecting in 30 seconds...")
            time.sleep(30)  # Wait before trying a new proxy/relay or reconnecting
        except Exception as e:
            print(f"Error during VPN connection: {e}. Retrying in 30 seconds...")
            time.sleep(30)  # Wait before retrying in case of error

# Run the automated VPN connection process
if __name__ == "__main__":
    automate_vpn_connection()
