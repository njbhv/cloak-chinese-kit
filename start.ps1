# CloakBrowser 出海版 - 一键初始化脚本
# 用法: 右键"以管理员身份运行"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  CloakBrowser 出海版 一键安装" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Docker
$dockerCheck = docker --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 未检测到 Docker Desktop" -ForegroundColor Red
    Write-Host "请先安装 Docker Desktop: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Docker: $dockerCheck" -ForegroundColor Green

# 检查 Git
$gitCheck = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 未检测到 Git" -ForegroundColor Red
    Write-Host "请先安装 Git: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Git: $gitCheck" -ForegroundColor Green

Write-Host ""
Write-Host "准备启动 CloakBrowser..." -ForegroundColor Yellow

# 启动
docker compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "  CloakBrowser 启动成功！" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "VNC 连接: localhost:5900 (密码: cloak2026)" -ForegroundColor White
    Write-Host "DevTools: ws://localhost:9222" -ForegroundColor White
    Write-Host ""
    Write-Host "查看状态: docker compose ps" -ForegroundColor Gray
    Write-Host "查看日志: docker compose logs -f" -ForegroundColor Gray
    Write-Host "停止: docker compose down" -ForegroundColor Gray
} else {
    Write-Host "❌ 启动失败，请检查 Docker 是否正在运行" -ForegroundColor Red
}
