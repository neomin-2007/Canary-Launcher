#!/bin/sh

pyinstaller --onefile \
    --add-data "assets/launcher.py:." \
    --add-data "assets/background.png:." \
    --add-data "assets/banner.png:." \
    --add-data "assets/icon.ico:." \
    --add-data "assets/icon.png:." \
    --add-data "assets/settings_icon.png:." \
    --add-data "assets/discord_icon.png:." \
    --icon="icon.png" \
    --clean \
    --windowed \
    --name="CanaryClient" \
    main.py