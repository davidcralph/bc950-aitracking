@echo off
setlocal

for /f "tokens=3" %%i in ('reg.exe query "HKLM\SOFTWARE\Microsoft\MSBuild\ToolsVersions\4.0" /v MSBuildToolsPath 2^>nul ^| findstr "MSBuildToolsPath"') do set "MSBuildPath=%%i"

set "currentDir=%CD:/=\%"
set "MSBuildPath=%MSBuildPath:"=%"

"%MSBuildPath%\MSBuild.exe" "%currentDir%\Logitech-BCC950-PTZ-Lib\PTZDevice.csproj" /p:Configuration=Release /p:Platform=x64 /p:PlatformToolset=v140 /p:OutDir="%currentDir%"
