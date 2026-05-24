#!/bin/bash
# CloakBrowser 一键启动脚本
# Entrypoint for Docker container

set -e

echo "=== CloakBrowser 出海版启动 ==="

# 1. 启动虚拟显示器
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1

# 2. 启动轻量桌面
fluxbox &
sleep 1

# 3. 启动 VNC 远程桌面
x11vnc -display :99 -forever -nopw -quiet -xkb &
echo "VNC running on port 5900"

# 4. 配置代理
PROXY_ARGS=""
if [ -n "$CLOAK_PROXY_HOST" ]; then
    PROXY_ARGS="--proxy-server=${CLOAK_PROXY_TYPE}://${CLOAK_PROXY_HOST}:${CLOAK_PROXY_PORT}"
    echo "Proxy configured: ${CLOAK_PROXY_TYPE}://${CLOAK_PROXY_HOST}:${CLOAK_PROXY_PORT}"
fi

# 5. 设置指纹配置文件
PROFILE_DIR="/app/profiles/${CLOAK_PROFILE}"
mkdir -p "$PROFILE_DIR"

# 6. 启动 CloakBrowser
echo "Starting CloakBrowser with profile: ${CLOAK_PROFILE}"
echo "VNC: connect to localhost:5900"
echo "DevTools: ws://localhost:9222"

# CloakBrowser 作为一个 Playwright 替代品运行
# 它提供 stealth Chromium 特性
# 通过 DevTools Protocol 管理
cd /app/cloak

# 以 headless 或 GUI 模式运行
if [ "$CLOAK_HEADLESS" = "true" ]; then
    # Headless 模式 - 用于自动化脚本
    ./cloak-browser \
        --headless=new \
        --remote-debugging-port=9222 \
        --user-data-dir="$PROFILE_DIR" \
        --no-sandbox \
        --disable-gpu \
        $PROXY_ARGS \
        --disable-blink-features=AutomationControlled \
        2>/tmp/cloak.log &
else
    # GUI 模式 - 可通过 VNC 查看
    ./cloak-browser \
        --remote-debugging-port=9222 \
        --user-data-dir="$PROFILE_DIR" \
        --no-sandbox \
        --disable-gpu \
        --window-size=1920,1080 \
        $PROXY_ARGS \
        --disable-blink-features=AutomationControlled \
        2>/tmp/cloak.log &
fi

CLOAK_PID=$!
echo "CloakBrowser PID: $CLOAK_PID"

# 7. 健康检查
sleep 3
if kill -0 $CLOAK_PID 2>/dev/null; then
    echo "CloakBrowser started successfully"
    echo ""
    echo "===================================="
    echo "  使用说明："
    echo "  - VNC 查看浏览器: localhost:5900"
    echo "  - DevTools: ws://localhost:9222"
    echo "  - 管理 API: http://localhost:8080"
    echo "===================================="
else
    echo "ERROR: CloakBrowser failed to start"
    cat /tmp/cloak.log
    exit 1
fi

# 8. 保持容器运行
wait $CLOAK_PID
