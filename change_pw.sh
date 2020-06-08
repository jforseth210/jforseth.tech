#!/bin/bash
# Change password
# user:password
echo "$1:$2" | chpasswd
