# EA SNIPER

A python script that uses EA's username availability API to check a list of usernames to see if they are taken or not. 

## Requirements
- **Python 3.x**: Download and install Python from [python.org](https://www.python.org/).
- **Required Libraries**: Install the required Python libraries using pip:
  ```bash
  pip install requests colorama

 ## File Formatting

### `usernames.txt`
- This file should contain the list of usernames you want to check.
- **Format**: One username per line.

### `proxies.txt`
- This file should contain the list of proxies you want to use. *PROXIES ARE REQUIRED FOR THIS SCRIPT*
- **Format**: One proxy per line in the format `ip:port`.

### `INFO`
- **This script is naturally slow, checking a username every 1-2 seconds. This is to prevent being rate limited by EA.**
