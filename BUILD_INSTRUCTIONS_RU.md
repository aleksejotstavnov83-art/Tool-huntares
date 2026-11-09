# HUNTARES TOOL — сборка APK

Исходный Android-проект с PAK/LUA-интерфейсом и Python-модулями.

## Termux: загрузка проекта в существующий репозиторий

1. Распакуй ZIP в отдельную папку (например через файловый менеджер).
2. В Termux:

```sh
pkg install git -y
cd ~/Tool-huntares
# Скопируй сюда содержимое распакованного ZIP, включая скрытую папку .github
git add -A
git commit -m "HUNTARES TOOL Android build"
git push origin main
```

## GitHub Actions

Открой репозиторий → Actions → Build Android APK → последний успешный запуск → Artifacts → HUNTARES-TOOL-debug-APK. Скачай архив артефакта и распакуй `app-debug.apk`.

## Ограничения

Это отладочная сборка, не проверенная на устройстве. Не все PAK и Lua совместимы. Система онлайн-ключей и админ-панель с сервером в данном ZIP не реализованы. Для продакшена нужны сервер, безопасная авторизация и подпись release APK.
