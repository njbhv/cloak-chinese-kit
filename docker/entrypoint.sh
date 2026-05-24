#!/bin/bash
# CloakBrowser ä¸€é”®å¯åŠ¨è„šæœ¬
# Entrypoint for Docker container

set -e

echo "=== CloakBrowser å‡ºæµ·ç‰ˆå¯åŠ¨ ==="

# 1. å¯åŠ¨è™šæ‹Ÿæ˜¾ç¤ºå™¨
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1

# 2. å¯åŠ¨è½»é‡æ¡Œé¢
fluxbox &
sleep 1

# 3. å¯åŠ¨ VNC è¿œç¨‹æ¡Œé¢
x11vnc -display :99 -forever -nopw -quiet -xkb &
echo "VNC running on port 5900"

# 4. é…ç½®ä»£ç†
PROXY_ARGS=""
if [ -n "$CLOAK_PROXY_HOST" ]; then
    PROXY_ARGS="--proxy-server=${CLOAK_PROXY_TYPE}://${CLOAK_PROXY_HOST}:${CLOAK_PROXY_PORT}"
    echo "Proxy configured: ${CLOAK_PROXY_TYPE}://${CLOAK_PROXY_HOST}:${CLOAK_PROXY_PORT}"
fi

# 5. è®¾ç½®æŒ‡çº¹é…ç½®æ–‡ä»¶ï¼ˆä»Žåªè¯»æ¨¡æ¿å¤åˆ¶åˆ°å¯å†™æ•°æ®ç›®å½•ï¼‰
PROFILE_TEMPLATE="/app/profiles/${CLOAK_PROFILE}.yaml"
PROFILE_DIR="/app/data/profiles/${CLOAK_PROFILE}"
mkdir -p "$PROFILE_DIR"

# 6. å¯åŠ¨ CloakBrowser
echo "Starting CloakBrowser with profile: ${CLOAK_PROFILE}"
echo "VNC: connect to localhost:5900"
echo "DevTools: ws://localhost:9222"

# CloakBrowser ä½œä¸ºä¸€ä¸ª Playwright æ›¿ä»£å“è¿è¡Œ
# å®ƒæä¾› stealth Chromium ç‰¹æ€§
# é€šè¿‡ DevTools Protocol ç®¡ç†
cd /app/cloak

# ä»¥ headless æˆ– GUI æ¨¡å¼è¿è¡Œ
if [ "$CLOAK_HEADLESS" = "true" ]; then
    # Headless æ¨¡å¼ - ç”¨äºŽè‡ªåŠ¨åŒ–è„šæœ¬
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
    # GUI æ¨¡å¼ - å¯é€šè¿‡ VNC æŸ¥çœ‹
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

# 7. å¥åº·æ£€æŸ¥
sleep 3
if kill -0 $CLOAK_PID 2>/dev/null; then
    echo "CloakBrowser started successfully"
    echo ""
    echo "===================================="
    echo "  ä½¿ç”¨è¯´æ˜Žï¼š"
    echo "  - VNC æŸ¥çœ‹æµè§ˆå™¨: localhost:5900"
    echo "  - DevTools: ws://localhost:9222"
    echo "  - ç®¡ç† API: http://localhost:8080"
    echo "===================================="
else
    echo "ERROR: CloakBrowser failed to start"
    cat /tmp/cloak.log
    exit 1
fi

# 8. ä¿æŒå®¹å™¨è¿è¡Œ
wait $CLOAK_PID
