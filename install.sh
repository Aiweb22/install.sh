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
wget https://linux.multitheftauto.com/dl/multitheftauto_linux_x64.tar.gz -O mtasa.tar.gz
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download MTA:SA server files! Please check the URL or your internet connection.${NC}"
    exit 1
fi

# Extract the downloaded files
tar -xvzf mtasa.tar.gz
rm mtasa.tar.gz

echo -e "* MTA:SA Server Installed"

# Check if MTA directory exists
if [ ! -d "multitheftauto_linux_x64" ]; then
    echo -e "${RED}MTA directory not found! The server may not have been installed correctly.${NC}"
    exit 1
fi

# Change to the MTA directory
cd multitheftauto_linux_x64/

# Check if mta-server exists
if [ ! -f "mta-server" ]; then
    echo -e "${RED}mta-server file not found! Please ensure the server was extracted correctly.${NC}"
    exit 1
fi

echo -e "* Starting MTA:SA Server"

# Start MTA:SA server
./mta-server &

echo -e "* MTA:SA Server is now running!"

# Optionally, configure the panel with Node.js (if you need to configure Draco Daemon or other services)
echo -e "* Setting up Node.js Panel (if applicable)"
cd /path/to/your/node-project  # Update this path with your actual node.js project directory
if [ ! -d "node_modules" ]; then
    npm install  # Install Node.js dependencies
fi

echo -e "* Running Node.js server configuration"

# Run the Node.js server (replace with actual panel setup if needed)
node . --panel http://localhost:3000 --key 8c539034-466d-4b81-931f-719f308e846e

echo -e "* Node.js server is now running!"
