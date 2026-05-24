# 🛡️ CloakBrowser 出海一键部署包

> **CloakBrowser**（GitHub 19.6K⭐）是基于 Chromium 的隐身浏览器，可绕过所有主流 Bot 检测。
> 本仓库提供**中文一键部署包**，让国内跨境电商、出海营销人员 5 分钟搭好环境。

---

## 🎯 适用人群

| 人群 | 场景 |
|------|------|
| 🏪 **跨境电商卖家** | 亚马逊/Shopify 多店铺管理、店铺养号 |
| 📱 **出海社媒运营** | TikTok/Instagram/Facebook 多账号运营 |
| 🔧 **独立开发者** | 爬虫/自动化采集需要反检测环境 |
| 📊 **市场调研** | 伪装成当地用户查看竞品信息 |

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
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/cloak-chinese-kit
cd cloak-chinese-kit

# 配置代理（可选）
.\scripts\proxy-setup.ps1 -Type socks5 -Host 1.2.3.4 -Port 1080

# 一键启动！
docker compose up -d
```

### 连接使用

| 方式 | 地址 | 用途 |
|------|------|------|
| 🔌 **VNC Viewer** | `localhost:5900` | 远程桌面浏览 |
| 🔧 **DevTools** | `ws://localhost:9222` | 自动化脚本 |
| 🌐 **浏览器** | 容器内打开 | 正常浏览 |

VNC 密码: `cloak2026`

---

## ⚙️ 配置详解

### 代理配置

```bash
# HTTP 代理
docker compose run -e CLOAK_PROXY_TYPE=http -e CLOAK_PROXY_HOST=代理IP -e CLOAK_PROXY_PORT=3128

# SOCKS5 代理（推荐）
docker compose run -e CLOAK_PROXY_TYPE=socks5 -e CLOAK_PROXY_HOST=代理IP -e CLOAK_PROXY_PORT=1080
```

### 切换指纹配置

```bash
# 亚马逊卖家模式
docker compose run -e CLOAK_PROFILE=amazon-seller

# TikTok 营销模式
docker compose run -e CLOAK_PROFILE=tiktok-marketer

# 通用社媒模式（默认）
docker compose run -e CLOAK_PROFILE=social-media-general
```

---

## 📁 项目结构

```
cloak-chinese-kit/
├── docker-compose.yml       # 一键启动
├── docker/
│   ├── Dockerfile           # 容器构建
│   └── entrypoint.sh        # 启动脚本
├── scripts/
│   ├── proxy-setup.ps1      # Windows 代理配置
│   └── proxy-setup.sh       # Linux/Mac 代理配置
├── profiles/
│   ├── amazon-seller.yaml   # 亚马逊指纹
│   ├── tiktok-marketer.yaml # TikTok 指纹
│   └── social-media-general.yaml # 通用指纹
└── docs/
    └── usage.md             # 详细使用说明
```

---

## 🛠️ 使用场景实例

### 场景 1：亚马逊多店铺管理

```bash
# 店1 - 美国站
docker compose -p shop-us up -d
# 店2 - 欧洲站 (改代理和指纹)
docker compose -p shop-eu up -d
```

### 场景 2：TikTok 批量运营

```bash
# 通过脚本启动多个独立实例
for i in 1 2 3 4 5; do
  docker compose -p tiktok-$i up -d
done
```

### 场景 3：Playwright 自动化

```javascript
const browser = await chromium.connectOverCDP('http://localhost:9222');
// CloakBrowser 自动处理指纹隐身
// 无需额外配置 stealth 插件
```

---

## 💰 版本对比

| 功能 | 免费版（当前） | Pro 版（$9.99） |
|------|---------------|-----------------|
| 基础部署 | ✅ | ✅ |
| 指纹模板 | 3 个 | 20 个+ |
| 代理集成 | 手动配置 | 一键脚本+代理池 |
| 多开管理 | 手动 docker | 管理面板 |
| 视频教程 | - | ✅ 5 分钟教程 |
| 技术支持 | GitHub Issues | 微信/Telegram 群 |

**购买 Pro 版：**
```text
TRON:    TCXucuhPXmk9abvhzJMu38SsnnVZwW3efa
Arbitrum: 0xb130639050DeDC444EbA69A1c19162Bf754e7CcA
Solana:  Fg8PiJaWB1Y9WeGG6fQJZp1K3GLiiQGFYMnqXLKSVEM1
Polygon: 0xB3F3a3DF81E57aacD13fe38e5C72765c4Ca0B47E
```

付款后发送 TXID 到 GitHub Issues 或 Telegram，24 小时内发送 Pro 激活包。

---

## 🤝 贡献

欢迎提 Issue 和 PR。  
目前需要帮助的：更多平台的指纹配置、英文文档翻译。

---

## 📜 免责声明

本工具仅用于合法的跨境业务、市场调研和自动化测试。  
请遵守各平台服务条款，使用者自行承担法律责任。

---

## ⭐ 支持一下

如果觉得有用，给个 Star ⭐ 支持开源！
