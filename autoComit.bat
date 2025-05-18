git --version
git add .
git commit -m "'function that correctly calls root.destroy() '"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v4.1
git push origin v4.1
pause
