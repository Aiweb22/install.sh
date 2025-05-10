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

# Download the MTA:SA server files from the correct URL
wget https://linux.multitheftauto.com/dl/multitheftauto_linux_x64.tar.gz -O mtasa.tar.gz
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download the MTA:SA server file!${NC}"
    exit 1
fi
tar -xvzf mtasa.tar.gz
rm mtasa.tar.gz

echo -e "* MTA:SA Server Installed"

# Find the MTA folder name and change directory to it
MTA_DIR=$(ls -d */ | grep -i 'multitheftauto' | head -n 1)
if [ -z "$MTA_DIR" ]; then
    echo -e "${RED}MTA directory not found!${NC}"
    exit 1
fi

echo -e "* Changing directory to $MTA_DIR"
cd "$MTA_DIR"

# List the files in the directory to confirm mta-server exists
echo -e "* Listing files in $MTA_DIR"
ls -l

# Check if the mta-server file exists
if [ -f "./mta-server" ]; then
    echo -e "* Starting MTA:SA Server"
    ./mta-server
    echo -e "* MTA:SA Server is now running!"
else
    echo -e "${RED}mta-server file not found in $MTA_DIR!${NC}"
    exit 1
fi

# Additional message to run `node .`
echo -e "* Run 'node .' to start the server."

