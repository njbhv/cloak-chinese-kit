# 🛡️ CloakBrowser 出海一键部署包

> **CloakBrowser**（GitHub 19.6K⭐）是基于 Chromium 的隐身浏览器，可绕过所有主流 Bot 检测。
> 本仓库提供**中文一键部署包**，让国内跨境电商、出海营销人员 5 分钟搭好环境。

---

## 🎯适用人群

| 人群 | 场景 |
|------|------|
| 🏪 跨境电商卖家 | 亚马逊/Shopify 多店铺管理、店铺养号 |
| 📱 出海社媒运营 | TikTok/Instagram/Facebook 多账号运营 |
| 🔧 独立开发者 | 爬虫/自动化采集需要反检测环境 |
| 📊 市场调研 | 伪装成当地用户查看竞品信息 |

---

## ✨ 特色

- ✅ **中文一键部署** — Docker Compose 一条命令启动
- ✅ **预置指纹模板** — 亚马逊/TikTok/通用社媒专用配置
- ✅ **代理集成** — 支持 HTTP/SOCKS5 代理
- ✅ **VNC 远程桌面** — 像操作本地浏览器一样操作
- ✅ **DevTools 集成** — 支持 Playwright/Puppeteer 自动化
- ✅ **全部开源免费** — 一键包免费，Pro 版 $9.99 更多功能

---

## 🚀 快速开始

### 前提
- 安装 Docker + Docker Compose
- 一个海外代理（如需，支持 HTTP/SOCKS5）

### 一步启动

```bash
git clone https://github.com/njbhv/cloak-chinese-kit
cd cloak-chinese-kit
docker compose up -d
```

### 连接使用

| 方式 | 地址 | 用途 |
|------|------|------|
| 🔌 VNC Viewer | localhost:5900 | 远程桌面浏览 |
| 🔧 DevTools | ws://localhost:9222 | 自动化脚本 |
| 🌐 浏览器 | 容器内打开 | 正常浏览 |

VNC 密码: cloak2026

---

## 💰 价格

| 功能 | 免费版 | Pro 版 ($9.99) |
|------|---------------|-----------------|
| 基础部署 | ✅ | ✅ |
| 指纹模板 | 3 个 | 20+ 个 |
| 代理集成 | 手动配置 | 一键脚本+代理池 |
| 多开管理 | 手动 docker | 管理面板 |
| 视频教程 | - | 5 分钟教程 |
| 技术支持 | GitHub Issues | 微信/Telegram 群 |

---

## 💸 付款方式

接受 TRON / Solana / Arbitrum / Polygon

```
TRON:    TCXucuhPXmk9abvhzJMu38SsnnVZwW3efa
Solana:  Fg8PiJaWB1Y9WeGG6fQJZp1K3GLiiQGFYMnqXLKSVEM1
Arbitrum: 0xb130639050DeDC444EbA69A1c19162Bf754e7CcA
Polygon:  0xB3F3a3DF81E57aacD13fe38e5C72765c4Ca0B47E
