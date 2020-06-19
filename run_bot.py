import os

import nonebot

import bot_config

base_dir = "."
plugins_dir = os.path.join(base_dir, "bot_plugins")
sukyaru_plugins_dir = os.path.join(plugins_dir, "sukyaru_bot")

if __name__ == "__main__":
    nonebot.init(bot_config)
    nonebot.load_plugins(
        plugin_dir=sukyaru_plugins_dir,
        module_prefix="bot_plugins.sukyaru_bot"
    )
    nonebot.run()