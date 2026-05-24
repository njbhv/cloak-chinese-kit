# CloakBrowser Pro - 隐身浏览器专业版

> 一次性付费 $9.99，终身使用。
> 超过免费版 20+ 指纹模板、代理池、多账号管理器。

## Pro 版包含

```
pro/
├── fingerprint_injector.py  ← CDP 指纹注入引擎（核心）
├── gen_profiles.py          ← 配置文件生成器
├── profiles/                ← 20 个指纹模板
│   ├── amazon-us.json       ← 亚马逊美国卖家
│   ├── amazon-uk.json       ← 亚马逊英国卖家
│   ├── amazon-jp.json       ← 亚马逊日本卖家
│   ├── shopify-general.json ← Shopify店主
│   ├── tiktok-shop.json     ← TikTok店铺
│   ├── tiktok-us.json       ← TikTok美国创作者
│   ├── instagram.json       ← Instagram运营
│   ├── facebook-ads.json    ← Facebook广告管理
│   ├── youtube-creator.json ← YouTube创作者
│   ├── linkedin.json        ← LinkedIn商务
│   ├── pinterest.json       ← Pinterest营销
│   ├── etsy-seller.json     ← Etsy卖家
│   ├── walmart-seller.json  ← Walmart卖家
│   ├── ebay-seller.json     ← eBay卖家
│   ├── ali-express.json     ← AliExpress卖家
│   ├── de-gdpr.json         ← 德国GDPR环境
│   ├── sg-user.json         ← 东南亚用户
│   ├── au-consumer.json     ← 澳洲用户
│   ├── br-shopper.json      ← 巴西用户
│   └── shopify-dropship.json ← 一件代发模式
└── scripts/
    └── proxy_pool.py        ← 代理池自动轮换+健康检查
```

## 使用

```bash
# 1. 列出所有指纹
python fingerprint_injector.py --list

# 2. 预览某个指纹配置
python fingerprint_injector.py --profile amazon-us

# 3. 应用到 CloakBrowser
python fingerprint_injector.py --apply --profile tiktok-us --ws ws://localhost:9222

# 4. 管理代理池
python scripts/proxy_pool.py add --proxy socks5://1.2.3.4:1080
python scripts/proxy_pool.py health-check
python scripts/proxy_pool.py rotate --name shop-us
```

## 购买

TRON:    TCXucuhPXmk9abvhzJMu38SsnnVZwW3efa
Solana:  Fg8PiJaWB1Y9WeGG6fQJZp1K3GLiiQGFYMnqXLKSVEM1
Arbitrum: 0xb130639050DeDC444EbA69A1c19162Bf754e7CcA
Polygon:  0xB3F3a3DF81E57aacD13fe38e5C72765c4Ca0B47E

付款后发 TXID 到 GitHub Issues，24 小时内收到 Pro 激活包。
