import os

import nonebot

import config

base_dir = "."
plugins_dir = os.path.join(base_dir, "plugins")
sukyaru_plugins_dir = os.path.join(plugins_dir, "sukyaru-bot")

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugins(
        plugin_dir=sukyaru_plugins_dir,
        module_prefix="plugins.sukyaru-bot"
    )
    nonebot.run()