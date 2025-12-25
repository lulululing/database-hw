# 快速启动脚本

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  销售数据分析系统 - 启动脚本" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python是否安装
Write-Host "检查Python环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python未安装，请先安装Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 检查依赖包
Write-Host "检查依赖包..." -ForegroundColor Yellow
$packages = @("streamlit", "pymysql", "pandas", "openpyxl")
$missing = @()

foreach ($package in $packages) {
    $check = python -c "import $package" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $package 已安装" -ForegroundColor Green
    } else {
        Write-Host "✗ $package 未安装" -ForegroundColor Red
        $missing += $package
    }
}

Write-Host ""

# 安装缺失的包
if ($missing.Count -gt 0) {
    Write-Host "正在安装缺失的包..." -ForegroundColor Yellow
    foreach ($package in $missing) {
        Write-Host "安装 $package..." -ForegroundColor Cyan
        pip install $package
    }
    Write-Host "✓ 依赖包安装完成" -ForegroundColor Green
    Write-Host ""
}

# 启动应用
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "启动应用..." -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "提示：" -ForegroundColor Cyan
Write-Host "1. 请确保已配置 config.py 中的数据库连接" -ForegroundColor White
Write-Host "2. 浏览器将自动打开 http://localhost:8501" -ForegroundColor White
Write-Host "3. 按 Ctrl+C 可停止服务器" -ForegroundColor White
Write-Host ""

# 运行Streamlit
streamlit run app.py
