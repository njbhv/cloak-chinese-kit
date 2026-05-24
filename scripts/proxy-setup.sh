#!/bin/bash
# CloakBrowser 代理配置脚本 (Linux/Mac)
# 用法: chmod +x proxy-setup.sh && ./proxy-setup.sh -t socks5 -h 1.2.3.4 -p 1080

while getopts "t:h:p:u:w:" opt; do
  case $opt in
    t) TYPE=$OPTARG ;;
    h) HOST=$OPTARG ;;
    p) PORT=$OPTARG ;;
    u) USER=$OPTARG ;;
    w) PASS=$OPTARG ;;
    *) echo "用法: $0 -t <http|socks5> -h <host> -p <port> [-u user] [-w pass]"; exit 1 ;;
  esac
done

cat > .env << EOF
CLOAK_PROXY_TYPE=${TYPE:-socks5}
CLOAK_PROXY_HOST=${HOST}
CLOAK_PROXY_PORT=${PORT:-1080}
CLOAK_PROXY_USER=${USER:-}
CLOAK_PROXY_PASS=${PASS:-}
CLOAK_PROFILE=default
CLOAK_HEADLESS=false
VNC_PASSWORD=cloak2026
EOF

echo "✅ Proxy configured: ${TYPE:-socks5}://${HOST}:${PORT:-1080}"
echo ""
echo "Start: docker compose up -d"
echo "VNC: localhost:5900 (password: cloak2026)"
