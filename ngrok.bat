@echo off
set ngrokPath=C:\ngrok

powershell -Command "$envPath = [System.Environment]::GetEnvironmentVariable('Path', [System.EnvironmentVariableTarget]::Machine); if ($envPath -notlike '*%ngrokPath%*') { $newEnvPath = '$envPath;%ngrokPath%'; [System.Environment]::SetEnvironmentVariable('Path', $newEnvPath, [System.EnvironmentVariableTarget]::Machine); Write-Output 'Caminho do ngrok.exe adicionado ao Path do sistema.' } else { Write-Output 'Caminho do ngrok.exe já está presente no Path do sistema.' }"