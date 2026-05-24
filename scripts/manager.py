#!/usr/bin/env python3
"""
CloakBrowser Multi-Account Manager (Pro version)
管理多个隐身浏览器实例，每个实例独立代理 + 指纹

用法:
  python manager.py add --name shop-us --proxy socks5://1.2.3.4:1080 --profile amazon-seller
  python manager.py start --name shop-us
  python manager.py list
  python manager.py stop --name shop-us
"""

import os, json, subprocess, sys, time
from pathlib import Path

CONFIG_DIR = Path.home() / ".cloak-manager"
CONFIG_FILE = CONFIG_DIR / "instances.json"

def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text("{}")

def load_instances():
    ensure_config()
    return json.loads(CONFIG_FILE.read_text())

def save_instances(instances):
    CONFIG_FILE.write_text(json.dumps(instances, indent=2))

def cmd_add(name, proxy, profile, port_offset):
    instances = load_instances()
    if name in instances:
        print(f"Error: instance '{name}' already exists")
        return
    instances[name] = {
        "proxy": proxy,
        "profile": profile,
        "vnc_port": 5900 + port_offset,
        "devtools_port": 9222 + port_offset,
        "status": "stopped"
    }
    save_instances(instances)
    print(f"Added instance '{name}'")

def cmd_start(name):
    instances = load_instances()
    if name not in instances:
        print(f"Error: instance '{name}' not found")
        return
    inst = instances[name]
    
    project_dir = Path(__file__).parent.parent
    compose_file = project_dir / "docker-compose.yml"
    
    env = os.environ.copy()
    if inst["proxy"]:
        proxy_parts = inst["proxy"].replace("://", "|").split("|")
        env["CLOAK_PROXY_TYPE"] = proxy_parts[0]
        env["CLOAK_PROXY_HOST"] = proxy_parts[1].split(":")[0]
        env["CLOAK_PROXY_PORT"] = proxy_parts[1].split(":")[1] if ":" in proxy_parts[1] else "1080"
    env["CLOAK_PROFILE"] = inst["profile"]
    
    cmd = f'docker compose -p cloak-{name} -f "{compose_file}" up -d'
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    if result.returncode == 0:
        inst["status"] = "running"
        inst["compose_project"] = f"cloak-{name}"
        save_instances(instances)
        print(f"Instance '{name}' started")
        print(f"  VNC:      localhost:{inst['vnc_port']}")
        print(f"  DevTools: ws://localhost:{inst['devtools_port']}")
    else:
        print(f"Failed to start '{name}': {result.stderr}")

def cmd_list():
    instances = load_instances()
    if not instances:
        print("No instances configured")
        return
    print(f"{'Name':<20} {'Profile':<25} {'Status':<10} {'VNC Port':<10}")
    print("-" * 65)
    for name, inst in instances.items():
        print(f"{name:<20} {inst['profile']:<25} {inst['status']:<10} {inst['vnc_port']:<10}")

def cmd_stop(name):
    instances = load_instances()
    if name not in instances:
        print(f"Error: instance '{name}' not found")
        return
    inst = instances[name]
    cmd = f'docker compose -p cloak-{name} down'
    subprocess.run(cmd, shell=True)
    inst["status"] = "stopped"
    save_instances(instances)
    print(f"Instance '{name}' stopped")

def cmd_batch(count, proxy_template, profile):
    """Batch create N instances with sequential proxy ports"""
    for i in range(count):
        proxy = proxy_template.replace("{i}", str(i + 1))
        name = f"account-{i+1:03d}"
        cmd_add(name, proxy, profile, i)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manager.py add --name <name> --proxy <proxy> --profile <profile> --offset <n>")
        print("  python manager.py start --name <name>")
        print("  python manager.py list")
        print("  python manager.py stop --name <name>")
        print("  python manager.py batch --count <n> --proxy <template> --profile <profile>")
        sys.exit(1)

    action = sys.argv[1]
    args = {sys.argv[i].lstrip("-"): sys.argv[i+1] for i in range(2, len(sys.argv)-1, 2)}

    if action == "add":
        cmd_add(args.get("name"), args.get("proxy"), args.get("profile", "social-media-general"), int(args.get("offset", "0")))
    elif action == "start":
        cmd_start(args.get("name"))
    elif action == "list":
        cmd_list()
    elif action == "stop":
        cmd_stop(args.get("name"))
    elif action == "batch":
        cmd_batch(int(args.get("count", "3")), args.get("proxy"), args.get("profile", "social-media-general"))
    else:
        print(f"Unknown action: {action}")
