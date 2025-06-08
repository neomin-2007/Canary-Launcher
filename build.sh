#!/bin/sh

pyinstaller --onefile \
    --add-data "updater.py:." \
    --add-data "launcher.py:." \
    --add-data "assets/background.png:assets" \
    --add-data "assets/banner.png:assets" \
    --add-data "assets/icon.ico:assets" \
    --add-data "assets/icon.png:assets" \
    --add-data "assets/modification_icon.png:assets" \
    --add-data "assets/settings_icon.png:assets" \
    --add-data "assets/discord_icon.png:assets" \
    --icon="assets/icon.png" \
    --clean \
    --windowed \
    --name="CanaryClient" \
    main.py