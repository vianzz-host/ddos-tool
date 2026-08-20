#!/bin/bash
# install.sh - Auto installer for DDoS Tool
# Developer: Vianzz Host

clear
echo -e "\033[31m"
echo " _    _______ ___    _   _ _____ _____ "
echo "| |  / /_  _//   |  / | / /__  //__  / "
echo "| | / / / / / /| | /  |/ /  / /   / /  "
echo "| |/ /_/ /_/ ___ |/ /|  /  / /__ / /__ "
echo "|___/_____/_/  |_/_/ |_/  /____//____/ "
echo "          _   _ _____ _____ _____ "
echo "         | | | /  _  // ___//_  _/ "
echo "         | |_| / / / /___ \   / /   "
echo "         |  _  / /_/ /____/  / /    "
echo "         |_| |_|____/_____/  /_/    "
echo -e "\033[0m"

echo -e "\033[36m╔═══════════════════════════════════════════════════╗"
echo -e "║  \033[33mINSTALLER DDOS TOOL - VIANZZ HOST       \033[36m║"
echo -e "╚═══════════════════════════════════════════════════╝\033[0m"

# Update packages
echo -e "\033[32m[+] Mengupdate packages...\033[0m"
pkg update -y && pkg upgrade -y

# Install Python if not exists
echo -e "\033[32m[+] Memastikan Python terinstall...\033[0m"
pkg install python -y

# Install pip
echo -e "\033[32m[+] Memastikan pip terinstall...\033[0m"
pkg install python-pip -y

# Install dependencies
echo -e "\033[32m[+] Menginstall dependencies...\033[0m"
pip install -r requirements.txt

# Install additional tools
echo -e "\033[32m[+] Menginstall tools tambahan...\033[0m"
pkg install git -y
pkg install tsu -y  # Untuk root access

# Set permission
chmod +x ddos.py

echo -e "\033[32m╔═══════════════════════════════════════════════════╗"
echo -e "║  \033[33mINSTALLASI SELESAI!                      \033[32m║"
echo -e "║  \033[36mJalankan: python ddos.py                 \033[32m║"
echo -e "╚═══════════════════════════════════════════════════╝\033[0m"
