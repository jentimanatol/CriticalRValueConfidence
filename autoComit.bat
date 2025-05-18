git --version
git add .
git commit -m "'UPDATE ICO IN TASCK BAR '"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v1.1
git push origin v1.1
pause
