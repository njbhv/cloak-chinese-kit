# CloakBrowser Docker Image
# åŸºäºŽ Ubuntuï¼Œè¿è¡Œéšèº« Chromium + VNC è¿œç¨‹æ¡Œé¢

FROM ubuntu:22.04

LABEL description="CloakBrowser - Stealth Chromium for Cross-Border E-commerce"
LABEL author="Cloak-Chinese-Kit"

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
ENV CLOAK_VERSION=latest

# å®‰è£…ä¾èµ–
RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb x11vnc fluxbox \
    fonts-wqy-zenhei fonts-wqy-microhei libcups2 \
    libnss3 libnspr4 libatk-bridge2.0-0 \
    libdrm2 libgbm1 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 \
    libpango-1.0-0 libcairo2 \
    libasound2 libatspi2.0-0 \
    locales \
    ca-certificates \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# å®‰è£… CloakBrowser
RUN mkdir -p /app/cloak && \
    cd /tmp && \
    curl -sL "https://github.com/CloakHQ/CloakBrowser/releases/latest/download/cloakbrowser-linux-x64.tar.gz" -o cloak.tar.gz && \
    tar xzf cloak.tar.gz && \
    mv chrome chrome_crashpad_handler chromedriver /app/cloak/ 2>/dev/null; \
    mv *.so *.pak *.bin *.dat *.json /app/cloak/ 2>/dev/null; \
    mv locales/ /app/cloak/ 2>/dev/null; \
    mv vk_swiftshader_icd.json /app/cloak/ 2>/dev/null; \
    rm -f cloak.tar.gz && \
    ls -la /app/cloak/ && \
    chmod +x /app/cloak/chrome && \
    ln -sf /app/cloak/chrome /app/cloak/cloak-browser

# ä¸­æ–‡è¯­è¨€æ”¯æŒ
RUN locale-gen zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8

ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN:zh
ENV LC_ALL=zh_CN.UTF-8

# å¯åŠ¨è„šæœ¬
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5900 9222 8080

CMD ["/entrypoint.sh"]
