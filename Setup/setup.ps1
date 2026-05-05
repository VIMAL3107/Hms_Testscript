# setup.ps1
# This script sets up the environment for the automated tests.
# It checks if components are already installed before trying to install them.

$ErrorActionPreference = "Stop"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   HMS Automation Setup Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check/Install Python
Write-Host "Checking Python..."
try {
    $pythonVersion = python --version 2>&1 | Select-Object -First 1
    if ($pythonVersion -match "Python") {
        Write-Host "[OK] Python is already installed ($pythonVersion)." -ForegroundColor Green
    } else {
        throw "Python not recognized"
    }
} catch {
    $wingetExists = Get-Command winget -ErrorAction SilentlyContinue
    if ($wingetExists) {
        Write-Host "[INSTALL] Python not found. Installing via winget..." -ForegroundColor Yellow
        winget install Python.Python.3.11 -e --silent --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "[INSTALL] winget not found. Downloading Python 3.11 installer..." -ForegroundColor Yellow
        $url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
        Invoke-WebRequest -Uri $url -OutFile "python-installer.exe"
        Write-Host "Installing Python..."
        Start-Process -FilePath "python-installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
        Remove-Item "python-installer.exe"
    }
    # Refresh env vars for this script
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 2. Check/Install Node.js
Write-Host "Checking Node.js..."
try {
    $nodeVersion = node -v 2>$null
    if ($nodeVersion) {
        Write-Host "[OK] Node.js is already installed ($nodeVersion)." -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    $wingetExists = Get-Command winget -ErrorAction SilentlyContinue
    if ($wingetExists) {
        Write-Host "[INSTALL] Node.js not found. Installing via winget..." -ForegroundColor Yellow
        winget install OpenJS.NodeJS -e --silent --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "[INSTALL] winget not found. Downloading Node.js installer..." -ForegroundColor Yellow
        $url = "https://nodejs.org/dist/v20.12.2/node-v20.12.2-x64.msi"
        Invoke-WebRequest -Uri $url -OutFile "node-installer.msi"
        Write-Host "Installing Node.js..."
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i node-installer.msi /quiet /norestart" -Wait
        Remove-Item "node-installer.msi"
    }
    # Refresh env vars for this script
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 2. Check/Install Java (JDK 17)
Write-Host "`nChecking Java (JDK)..."
try {
    $javaCmd = Get-Command java -ErrorAction SilentlyContinue
    if ($javaCmd) {
        $oldEA = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        $javaVersion = java -version 2>&1 | Select-Object -First 1
        $ErrorActionPreference = $oldEA
        Write-Host "[OK] Java is already installed ($javaVersion)." -ForegroundColor Green
    } else {
        throw "Java not recognized"
    }
} catch {
    $wingetExists = Get-Command winget -ErrorAction SilentlyContinue
    if ($wingetExists) {
        Write-Host "[INSTALL] Java JDK not found. Installing via winget..." -ForegroundColor Yellow
        winget install Microsoft.OpenJDK.17 -e --silent --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "[INSTALL] winget not found. Downloading Java JDK 17 installer..." -ForegroundColor Yellow
        $url = "https://aka.ms/download-jdk/microsoft-jdk-17-windows-x64.msi"
        Invoke-WebRequest -Uri $url -OutFile "jdk-installer.msi"
        Write-Host "Installing Java JDK..."
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i jdk-installer.msi /quiet /norestart" -Wait
        Remove-Item "jdk-installer.msi"
    }
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 3. Check/Install Appium
Write-Host "`nChecking Appium..."
try {
    $appiumVersion = appium -v 2>$null
    if ($appiumVersion) {
        Write-Host "[OK] Appium is already installed ($appiumVersion)." -ForegroundColor Green
    } else {
        throw "Appium not found"
    }
} catch {
    Write-Host "[INSTALL] Appium not found. Installing globally via npm..." -ForegroundColor Yellow
    npm install -g appium
}

# 4. Check/Install Appium UiAutomator2 Driver
Write-Host "`nChecking Appium UiAutomator2 Driver..."

# Appium often writes harmless warnings to stderr, which triggers our strict error catch.
# We temporarily relax error handling for this specific check.
$oldErrorAction = $ErrorActionPreference
$ErrorActionPreference = "Continue"

$drivers = appium driver list --installed 2>&1 | Out-String

if ($drivers -match "uiautomator2") {
    Write-Host "[OK] Appium UiAutomator2 driver is already installed." -ForegroundColor Green
} else {
    Write-Host "[INSTALL] Appium UiAutomator2 driver missing. Installing..." -ForegroundColor Yellow
    appium driver install uiautomator2
}

# Restore strict error handling
$ErrorActionPreference = $oldErrorAction

# 5. Check/Install Android SDK
Write-Host "`nChecking Android SDK..."
$SdkDir = "$env:LOCALAPPDATA\Android\Sdk"
$PlatformToolsDir = "$SdkDir\platform-tools"

if (Test-Path "$PlatformToolsDir\adb.exe") {
    Write-Host "[OK] Android SDK already exists (found via Android Studio or manual install)." -ForegroundColor Green
} else {
    Write-Host "[INSTALL] Android SDK not found. Downloading Command Line Tools..." -ForegroundColor Yellow
    
    New-Item -ItemType Directory -Force -Path "$SdkDir\cmdline-tools" | Out-Null
    $ZipPath = "$SdkDir\cmdline-tools.zip"
    
    # Download Android CMD line tools for Windows
    $DownloadUrl = "https://dl.google.com/android/repository/commandlinetools-win-10406996_latest.zip"
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipPath
    
    Write-Host "Extracting Android Tools..."
    Expand-Archive -Path $ZipPath -DestinationPath "$SdkDir\cmdline-tools" -Force
    Remove-Item $ZipPath
    
    # The extracted folder is named "cmdline-tools". We fix the structure to match the standard Android format.
    Rename-Item -Path "$SdkDir\cmdline-tools\cmdline-tools" -NewName "latest"
    
    Write-Host "[OK] Android SDK installed." -ForegroundColor Green
}

# 6. Check/Set Environment Variables Permanently (if not set)
Write-Host "`nChecking Environment Variables..."
$CurrentAndroidHome = [System.Environment]::GetEnvironmentVariable("ANDROID_HOME", "User")
if ($CurrentAndroidHome -eq $SdkDir) {
    Write-Host "[OK] ANDROID_HOME is already set." -ForegroundColor Green
} else {
    Write-Host "[SETUP] Setting ANDROID_HOME environment variable permanently..." -ForegroundColor Yellow
    [System.Environment]::SetEnvironmentVariable("ANDROID_HOME", $SdkDir, "User")
}

Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host " Setup Complete! You can now run the app." -ForegroundColor Cyan
Write-Host " Note: You may need to restart your terminal or computer" -ForegroundColor Cyan
Write-Host " if this was your very first time installing Node/Java." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

Pause
