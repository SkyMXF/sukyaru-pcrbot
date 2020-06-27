from nonebot import on_command, CommandSession
import nonebot

import random

from .lib import configs
import bot_config
from main import utils

fk_list = [
    "你🐴的，老娘不是臭鼬是猫猫",
    "哦吼又叫我臭鼬是吧，你这个B水黑春黑必#",
    "爬",
    "👊👊👊给老娘滚",
    "你才臭鼬，你全家都臭鼬",
    "吃我格林爆炸，给👴死"
]
hello_list = [
    "骑士君你好呀~",
    "骑士君你好呀，今天有没有度过开心的一天呢~",
    "喵噜噜噜zzzzzzzz....!!!\n诶，有人叫我么"
]

@on_command(name="sukanku", aliases=(r".*臭鼬.*"), only_to_me=False)
async def sukanku(session: CommandSession):


    await session.send(
        random.choice(fk_list)
    )

@sukanku.args_parser
async def sukanku_parser(session: CommandSession):
    
    pass

@on_command(name="kyaru", aliases=(r"凯露.*", r"凯露酱.*"), only_to_me=False)
async def kyaru(session: CommandSession):

    await session.send(
        random.choice(hello_list)
    )

@kyaru.args_parser
async def kyaru_parser(session: CommandSession):

    pass