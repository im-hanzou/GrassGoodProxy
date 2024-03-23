import json
import requests
import re  

def extract_ip_and_format(line):
    pattern = r'(?:http|socks4|socks5)://(?:\w*:?[\w]*@)?([\d\.]+:\d+)'
    match = re.search(pattern, line)
    if match:
        return match.group(1), line.strip()  
    return None, None

def read_proxy_file(filename):
    """Membaca file proxy dan menyimpannya dalam dictionary."""
    proxy_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            ip_port, original_format = extract_ip_and_format(line)
            if ip_port:
                proxy_dict[ip_port] = original_format  
    return proxy_dict

def main():
    cookie_file = "cookie.json"
    proxy_file = "proxy.txt"
    output_file = "ipgood.txt"

    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "id,en-US;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": cookie_string
    }
    
    response = requests.get("https://api.getgrass.io/users/dash", headers=headers)
    data = response.json()
    
    devices = data.get('data', {}).get('devices', [])
    proxy_data = read_proxy_file(proxy_file)

    with open(output_file, 'w') as outfile:
        for device in devices:
            if device.get("final_score", 0) != 0:
                ip_prefix = ".".join(device.get("device_ip").split('.')[:1])  
                ip_found = False
                for ip_port, original_format in proxy_data.items():
                    proxy_ip_prefix = ".".join(ip_port.split(':')[0].split('.')[:1])  
                    if ip_prefix == proxy_ip_prefix:
                        outfile.write(original_format + "\n")  
                        print(f"Format proxy untuk IP {device.get('device_ip')} disimpan.")
                        ip_found = True
                        break
                #if not ip_found:
                    #outfile.write(device.get("device_ip") + "\n")
                    #print(f"IP {device.get('device_ip')} disimpan karena tidak ditemukan dalam proxy.txt.")

if __name__ == "__main__":
    main()
