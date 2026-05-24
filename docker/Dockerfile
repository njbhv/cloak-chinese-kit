# CloakBrowser Docker Image
# 基于 Ubuntu，运行隐身 Chromium + VNC 远程桌面

FROM ubuntu:22.04

LABEL description="CloakBrowser - Stealth Chromium for Cross-Border E-commerce"
LABEL author="Cloak-Chinese-Kit"

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
ENV CLOAK_VERSION=latest

# 安装依赖
RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb x11vnc fluxbox \
    fonts-wqy-zenhei fonts-wqy-microhei \
    libnss3 libnspr4 libatk-bridge2.0-0 \
    libdrm2 libgbm1 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 \
    libpango-1.0-0 libcairo2 \
    libasound2 libatspi2.0-0 \
    ca-certificates \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 CloakBrowser
RUN mkdir -p /app && \
    cd /app && \
    # CloakBrowser 发布版本会自动下载
    curl -sL "https://github.com/CloakHQ/CloakBrowser/releases/latest/download/cloak-linux.zip" -o cloak.zip && \
    unzip -q cloak.zip -d /app/cloak && \
    rm cloak.zip && \
    chmod +x /app/cloak/cloak-browser

# 中文语言支持
RUN locale-gen zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8

ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN:zh
ENV LC_ALL=zh_CN.UTF-8

# 启动脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5900 9222 8080

CMD ["/entrypoint.sh"]
