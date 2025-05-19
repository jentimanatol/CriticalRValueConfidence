git --version
git add .
git commit -m "'UPDATE worck flow file for GitHub Actions'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v1.9
git push origin v1.9
pause
