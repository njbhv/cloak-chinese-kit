#!/usr/bin/env python3
"""
CloakBrowser Proxy Pool Manager
Auto-rotate proxies with health checks
Usage: python proxy_pool.py add --proxy socks5://user:pass@1.2.3.4:1080
       python proxy_pool.py list
       python proxy_pool.py rotate --name account-001
"""

import json, subprocess, sys, time, random, re
from pathlib import Path
from datetime import datetime

CONFIG_DIR = Path.home() / ".cloak-proxy-pool"
CONFIG_FILE = CONFIG_DIR / "pool.json"

def ensure():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps({"proxies": [], "last_rotation": {}}))

def load():
    ensure()
    return json.loads(CONFIG_FILE.read_text())

def save(data):
    CONFIG_FILE.write_text(json.dumps(data, indent=2))

def health_check(proxy):
    try:
        import urllib.request
        # Test with a fast-responding site
        req = urllib.request.Request("http://httpbin.org/ip", timeout=5)
        if "@" in proxy:
            # Extract auth
            auth_part = proxy.split("@")[0].split("://")[1]
            user_pass = auth_part.split(":")
            import base64
            credentials = base64.b64encode(f"{user_pass[0]}:{user_pass[1]}".encode()).decode()
            req.add_header("Proxy-Authorization", f"Basic {credentials}")
        
        proxy_handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
        opener = urllib.request.build_opener(proxy_handler)
        resp = opener.open(req)
        ip = resp.read().decode()
        import re
        ip_match = re.search(r'"origin":\s*"([^"]+)"', ip)
        return ip_match.group(1) if ip_match else "unknown"
    except Exception as e:
        return None

def cmd_add(proxy_str):
    data = load()
    # Validate format
    if not proxy_str.startswith(("socks5://", "http://", "https://")):
        print("Invalid format. Use: socks5://user:pass@host:port or http://host:port")
        return
    data["proxies"].append({"url": proxy_str, "status": "pending", "added": datetime.now().isoformat()})
    save(data)
    print(f"Added proxy ({len(data['proxies'])} total): {proxy_str}")

def cmd_list():
    data = load()
    if not data["proxies"]:
        print("No proxies in pool")
        return
    print(f"{'#':<4} {'Status':<10} {'URL':<50}")
    print("-" * 64)
    for i, p in enumerate(data["proxies"]):
        url = p["url"]
        if len(url) > 45:
            url = url[:42] + "..."
        print(f"{i+1:<4} {p.get('status','?') :<10} {url:<50}")

def cmd_health_check_all():
    data = load()
    if not data["proxies"]:
        print("No proxies to check")
        return
    for i, p in enumerate(data["proxies"]):
        print(f"Checking #{i+1}: {p['url'][:40]}... ", end="")
        ip = health_check(p["url"])
        if ip:
            p["status"] = f"ok ({ip})"
            print(f"OK ({ip})")
        else:
            p["status"] = "dead"
            print("DEAD")
        data["proxies"][i] = p
        time.sleep(1)  # Rate limit
    save(data)

def cmd_rotate(instance_name):
    data = load()
    alive = [p for p in data["proxies"] if p.get("status", "").startswith("ok")]
    if not alive:
        print("No healthy proxies. Run health-check first.")
        return
    
    proxy = random.choice(alive)
    data["last_rotation"][instance_name] = {"proxy": proxy["url"], "at": datetime.now().isoformat()}
    save(data)
    print(f"Rotated {instance_name} -> {proxy['url']}")
    print(f"\nTo apply: set env vars and restart:")
    print(f"  CLOAK_PROXY={proxy['url']}")

def cmd_import_file(path):
    with open(path) as f:
        lines = f.read().strip().split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            cmd_add(line)
    print(f"Imported {len(lines)} proxies from {path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python proxy_pool.py add --proxy socks5://user:pass@1.2.3.4:1080")
        print("  python proxy_pool.py import --file proxies.txt")
        print("  python proxy_pool.py list")
        print("  python proxy_pool.py health-check")
        print("  python proxy_pool.py rotate --name shop-us")
        sys.exit(1)
    
    action = sys.argv[1]
    args = {}
    for i in range(2, len(sys.argv)-1, 2):
        key = sys.argv[i].lstrip("-")
        args[key] = sys.argv[i+1]
    
    if action == "add": cmd_add(args.get("proxy", ""))
    elif action == "import": cmd_import_file(args.get("file", ""))
    elif action == "list": cmd_list()
    elif action == "health-check": cmd_health_check_all()
    elif action == "rotate": cmd_rotate(args.get("name", "default"))
    else: print(f"Unknown: {action}")
