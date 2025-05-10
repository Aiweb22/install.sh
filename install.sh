#!/bin/bash

# Update and install dependencies
echo "Updating package list and installing dependencies..."

# Install Node.js (for Ubuntu/Debian systems)
sudo apt update -y
sudo apt install -y nodejs npm git curl

# Check Node.js and npm installation
echo "Checking Node.js and npm versions..."
node -v
npm -v

# Clone your repository (replace with your repository URL)
echo "Cloning the project repository..."
git clone https://github.com/your-username/your-repository.git /path/to/project/folder

# Navigate to the project directory
cd /path/to/project/folder

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Set custom port
CUSTOM_PORT=8080

# Modify the server.js file to use the custom port
echo "Setting custom port to $CUSTOM_PORT in server.js..."
sed -i "s/const port = .*/const port = process.env.PORT || $CUSTOM_PORT;/g" server.js

# Set up MTA server (replace with your MTA server installation steps)
echo "Setting up MTA server..."
# (Install and configure your MTA server here if needed)

# Create Dockerfile if you plan to use Docker
echo "Creating Dockerfile..."
cat > Dockerfile <<EOL
FROM node:14

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

# Expose custom port (e.g., 8080)
EXPOSE $CUSTOM_PORT

CMD ["node", "server.js"]
EOL

# Build Docker container (if applicable)
echo "Building Docker image..."
docker build -t mta-panel .

# Run the server (optional if Docker is used)
echo "Running the panel server on port $CUSTOM_PORT..."
docker run -p $CUSTOM_PORT:$CUSTOM_PORT mta-panel

echo "Installation complete! Visit http://localhost:$CUSTOM_PORT to access the panel."
