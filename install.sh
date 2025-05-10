#!/bin/bash

# ASCII Art
ascii_art="
---

| \ | |     | |      | |
|  | | __ *| | __***| |**
| . \` |/ _\` | |/ / **| '* \\
| |\  | (*| |   <_* \ | | |
|*| \_|\_*,*|*|\___/*| |\_|

"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Clear the screen
clear

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run this script as root.${NC}"
  exit 1
fi

echo -e "${CYAN}$ascii_art${NC}"

echo -e "* Installing Dependencies"

# Update package list and install dependencies
sudo apt update
sudo apt install -y curl software-properties-common git
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install nodejs -y

echo -e "* Installed Dependencies"

echo -e "* Downloading MTA:SA Server"

# Download the MTA:SA server files
wget https://mirror.multitheftauto.com/mta/mtasa_linux_x64.tar.gz -O mtasa.tar.gz
tar -xvzf mtasa.tar.gz
rm mtasa.tar.gz

echo -e "* MTA:SA Server Installed"

# Optional: Copy a pre-configured server config (adjust path as needed)
# cp /path/to/your/server.conf ./MTA/

echo -e "* Starting MTA:SA Server"

# Start MTA:SA server (you might need to adjust the path depending on your setup)
cd MTA
./mta-server

echo -e "* MTA:SA Server is now running!"
echo -e "* Run 'node .' to start the server."
