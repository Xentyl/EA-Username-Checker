import requests
import time
import random
import threading
from colorama import Fore, Style, init

init()

username_file = "usernames.txt"
proxy_file = "proxies.txt"
available_file = "available_usernames.txt"
api_url = "https://signin.ea.com/p/ajax/user/checkOriginId"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

session = requests.Session()
stop_script = False

def print_banner():
    banner = """
    ███████╗ █████╗     ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ 
    ██╔════╝██╔══██╗    ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
    █████╗  ███████║    ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
    ██╔══╝  ██╔══██║    ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
    ███████╗██║  ██║    ███████║██║ ╚████║██║██║     ███████╗██║  ██║
    ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
    """
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}EA Username Checker{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Press Enter to start...{Style.RESET_ALL}\n")

def stop_listener():
    global stop_script
    input("Press Enter to stop the script...\n")
    stop_script = True

def load_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = file.read().splitlines()
    return proxies

def test_proxy(proxy):
    try:
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=10
        )
        response.raise_for_status()
        print(f"Proxy {proxy} is working. IP: {response.json()['origin']}")
        return True
    except requests.exceptions.RequestException:
        print(f"{Fore.CYAN}Proxy {proxy} has failed to connect{Style.RESET_ALL}")
        return False

def check_username_availability(username, proxies):
    params = {
        "requestorId": "portal",
        "originId": username,
        "_": str(int(time.time() * 1000))
    }
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.ea.com/",
    }
    
    retries = 3
    for attempt in range(retries):
        proxy = random.choice(proxies)
        if not test_proxy(proxy):
            proxies.remove(proxy)
            continue
        
        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        try:
            response = session.get(api_url, params=params, headers=headers, proxies=proxy_dict, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") is True:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            print(f"{Fore.CYAN}Proxy {proxy} failed to connect - connecting attempt {attempt + 1}{Style.RESET_ALL}")
            time.sleep(random.randint(1, 2))
    
    try:
        print(f"{Fore.CYAN}Falling back to direct connection for username {username}{Style.RESET_ALL}")
        response = session.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") is True:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        print(f"{Fore.CYAN}Fallback attempt failed for username {username}{Style.RESET_ALL}")
        return None

def save_available_usernames(available_usernames):
    with open(available_file, "w") as file:
        for username in available_usernames:
            file.write(f"{username}\n")

def update_username_file(checked_usernames):
    with open(username_file, "r") as file:
        usernames = file.read().splitlines()
    
    updated_usernames = [username for username in usernames if username not in checked_usernames]
    
    with open(username_file, "w") as file:
        for username in updated_usernames:
            file.write(f"{username}\n")

def check_usernames_from_file(file_path, proxy_file):
    global stop_script
    
    proxies = load_proxies(proxy_file)
    if not proxies:
        print("No proxies found in proxies.txt. Exiting.")
        return
    
    with open(file_path, "r") as file:
        usernames = file.read().splitlines()
    
    available_usernames = []
    checked_usernames = []
    
    stop_thread = threading.Thread(target=stop_listener)
    stop_thread.daemon = True
    stop_thread.start()
    
    print("Script started. Press Enter to stop and save progress.")
    
    for username in usernames:
        if stop_script:
            print("\nScript stopped by user.")
            break
        
        result = check_username_availability(username, proxies)
        if result is True:
            print(f"{Fore.GREEN}Username '{username}' is AVAILABLE{Style.RESET_ALL}")
            available_usernames.append(username)
        elif result is False:
            print(f"{Fore.RED}Username '{username}' is TAKEN{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Username '{username}' could not be checked due to errors{Style.RESET_ALL}")
        
        checked_usernames.append(username)
        time.sleep(random.randint(1, 3))
    
    save_available_usernames(available_usernames)
    update_username_file(checked_usernames)
    print(f"Saved {len(available_usernames)} available usernames to {available_file}.")
    print(f"Removed checked usernames from {username_file}.")

if __name__ == "__main__":
    print_banner()
    input()  # Wait for Enter to start
    check_usernames_from_file(username_file, proxy_file)