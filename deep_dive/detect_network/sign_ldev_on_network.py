import subprocess


def get_network_info():
    result = subprocess.run(['iwgetid'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    if 'ESSID' in output:
        essid = output.split('"')[1]
        result = subprocess.run(['ip', 'addr', 'show', 'dev', 'wlan0'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        ip_addr = output.split('inet ')[1].split('/')[0]
        return essid, ip_addr
    return None, None


def generate_ldevid():
    essid, ip_addr = get_network_info()
    if essid and ip_addr:
        print(f'Generating LDevID for network "{essid}" with IP address {ip_addr}')
        # Add code here to generate LDevID with network information
    else:
        print('Network not recognized. LDevID not generated.')


def main():
    generate_ldevid()

if __name__ == '__main__':
    main()
