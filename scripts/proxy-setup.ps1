# CloakBrowser 代理配置脚本
# 用法: .\proxy-setup.ps1 -Type http -Host 1.2.3.4 -Port 3128 -User username -Pass password

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("http", "socks5", "socks4")]
    [string]$Type = "socks5",
    
    [Parameter(Mandatory=$true)]
    [string]$Host,
    
    [Parameter(Mandatory=$true)]
    [int]$Port = 1080,
    
    [Parameter(Mandatory=$false)]
    [string]$User = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Pass = ""
)

$envFile = ".env"
$content = @"
CLOAK_PROXY_TYPE=$Type
CLOAK_PROXY_HOST=$Host
CLOAK_PROXY_PORT=$Port
CLOAK_PROXY_USER=$User
CLOAK_PROXY_PASS=$Pass
CLOAK_PROFILE=default
CLOAK_HEADLESS=false
VNC_PASSWORD=cloak2026
"@

$content | Out-File -FilePath $envFile -Encoding UTF8
Write-Host "✅ 代理已配置: $($Type)://$($Host):$($Port)"
Write-Host ""
Write-Host "启动: docker compose up -d"
Write-Host "查看运行状态: docker compose ps"
Write-Host "查看日志: docker compose logs -f"
Write-Host ""
Write-Host "VNC 连接: 打开 VNC Viewer → localhost:5900"
Write-Host "密码: cloak2026"
