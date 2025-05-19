git --version
git add .
git commit -m "'UPDATE worck flow file for GitHub Actions'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.0
git push origin v2.0
pause
