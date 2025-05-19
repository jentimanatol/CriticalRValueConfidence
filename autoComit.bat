git --version
git add .
git commit -m "'UPDATE ICO IN TASCK BAR ico size max 250*250 '"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v1.7
git push origin v1.7
pause
