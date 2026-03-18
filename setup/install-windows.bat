@echo off
:: MPDF File Type Registration for Windows
:: Associates .mpdf files with Microsoft Edge

echo Registering .mpdf file type...

reg add "HKCU\Software\Classes\.mpdf" /ve /d "mpdffile" /f >nul 2>&1
reg add "HKCU\Software\Classes\.mpdf" /v "Content Type" /d "text/html" /f >nul 2>&1
reg add "HKCU\Software\Classes\.mpdf" /v "PerceivedType" /d "text" /f >nul 2>&1
reg add "HKCU\Software\Classes\mpdffile" /ve /d "MPDF Document" /f >nul 2>&1
reg add "HKCU\Software\Classes\mpdffile\shell\open" /ve /d "Open in Browser" /f >nul 2>&1
reg add "HKCU\Software\Classes\mpdffile\shell\open\command" /ve /d "\"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe\" \"%%1\"" /f >nul 2>&1

echo.
echo Done! .mpdf files are now associated with Microsoft Edge.
echo Double-click any .mpdf file to open it.
pause
