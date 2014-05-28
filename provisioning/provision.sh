#!/bin/bash

set -e # Exit script immediately on first error.
set -x # Print commands and their arguments as they are executed.

# redis
sudo apt-get -y install redis-server

# forever
sudo npm install -g forever
