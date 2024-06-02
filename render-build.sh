#!/bin/bash

# Update and install dependencies
apt-get update && apt-get install -y wget unzip xvfb libxi6 libgconf-2-4

# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get -y install ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/local/bin/
