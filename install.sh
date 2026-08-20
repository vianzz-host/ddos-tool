#!/bin/bash
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
echo -e "║  \033[33mDDOS TOTAL - VIANZZ HOST               \033[36m║"
echo -e "╚═══════════════════════════════════════════════════╝\033[0m"

echo -e "\033[32m[+] Mengupdate packages...\033[0m"
pkg update -y && pkg upgrade -y

echo -e "\033[32m[+] Install Python...\033[0m"
pkg install python python-pip git -y

echo -e "\033[32m[+] Install dependencies...\033[0m"
pip install -r requirements.txt

echo -e "\033[32m[+] Set permission...\033[0m"
chmod +x ddos_vianzz.py

echo -e "\033[32m╔═══════════════════════════════════════════════════╗"
echo -e "║  \033[33mINSTALLASI SELESAI!                      \033[32m║"
echo -e "║  \033[36mJalankan: python ddos_vianzz.py        \033[32m║"
echo -e "╚═══════════════════════════════════════════════════╝\033[0m"
