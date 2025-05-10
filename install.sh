#!/bin/bash

echo "🛠 Installing Docker..."
sudo apt update
sudo apt install -y docker.io docker-compose

echo "✅ Docker installed."

# Create project folder
mkdir -p mta-docker/panel
mkdir -p mta-docker/mta

cd mta-docker

echo "📦 Setting up MTA Dockerfile..."
cat > mta/Dockerfile <<EOF
FROM ubuntu:20.04

RUN apt update && apt install -y wget unzip screen libpcre3 libpcre3-dev libxml2

WORKDIR /opt

RUN wget https://linux.mtasa.com/dl/153/multitheftauto_linux_x64-1.5.3.tar.gz && \\
    tar -xvzf multitheftauto_linux_x64-1.5.3.tar.gz

WORKDIR /opt/multitheftauto_linux_x64-1.5.3

CMD ["screen", "-dmS", "mta", "./mta-server64"]
EOF

echo "⚙️ Setting up Node.js panel Dockerfile..."
cat > panel/Dockerfile <<EOF
FROM node:18

WORKDIR /app
COPY . .

RUN npm install

EXPOSE 3000
CMD ["node", "server.js"]
EOF

echo "🧠 Writing panel server.js..."
cat > panel/server.js <<EOF
const express = require('express');
const { exec } = require('child_process');
const app = express();

app.get('/start', (req, res) => {
    exec('docker start mta-server', (err, stdout, stderr) => {
        res.send(stdout || stderr);
    });
});

app.get('/stop', (req, res) => {
    exec('docker stop mta-server', (err, stdout, stderr) => {
        res.send(stdout || stderr);
    });
});

app.listen(3000, () => {
    console.log('✅ Panel running at http://localhost:3000');
});
EOF

echo "📦 Initializing Node panel..."
cd panel
npm init -y
npm install express
cd ..

echo "📦 Writing docker-compose.yml..."
cat > docker-compose.yml <<EOF
version: '3'

services:
  mta-server:
    build:
      context: ./mta
    container_name: mta-server
    tty: true

  panel:
    build:
      context: ./panel
    container_name: mta-panel
    ports:
      - "3000:3000"
    depends_on:
      - mta-server
EOF

echo "🚀 Starting containers..."
docker-compose up -d --build

echo "✅ Done. Visit http://localhost:3000 to control your MTA server!"
