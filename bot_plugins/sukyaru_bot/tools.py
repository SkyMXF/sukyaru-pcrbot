from nonebot import on_command, CommandSession
import nonebot

import pytz
import datetime

from .lib import configs
import bot_config
from main import utils

cal_mine_example = "挖矿计算 15001"
@on_command(name="cal_mine", aliases=("挖矿计算"))
async def cal_mine(session: CommandSession):

    try:
        session.state["now_best_rank"] = int(session.state["now_best_rank"])
    except:
        await session.send("计算失败：输入格式有误噢~示例：%s"%(cal_mine_example))

    season_diam, all_season_diam = utils.cal_mine(session.state["now_best_rank"])

    await session.send(
        "当前赛季剩余钻石：%d, 总剩余钻石(含当前赛季)：%d，请确认输入的排名是当前赛季最高记录(不是当前排名)"%(season_diam, all_season_diam)
    )

@cal_mine.args_parser
async def cal_miner_parser(session: CommandSession):
    
    arg_text = session.current_arg_text.strip()
    session.state["now_best_rank"] = arg_text

@on_command(name="jjc_query", aliases=("JJC查询", "jjc查询"))
async def jjc_query(session: CommandSession):

    await session.send(
        "目前没有比较好的实现方式，可以直接去这个链接：https://pcrdfans.com/battle 进行查询"
    )

@jjc_query.args_parser
async def jjc_query_parser(session: CommandSession):
    
    #arg_text = session.current_arg_text.strip()
    return

guild_url = "http://101.200.128.60:8081/"
@on_command(name="get_url", aliases=("网址", "地址", "网站", "公会网站"))
async def get_url(session: CommandSession):
    await session.send(
        "凯露酱的公会档案馆：%s\n使用QQ昊即可登路，初始蜜马为123456，不写错别字就会被当成骗子封号555555"%(guild_url)
    )

@get_url.args_parser
async def get_url_parser(session: CommandSession):
    
    #arg_text = session.current_arg_text.strip()
    return

async def send_potion_remind():
    bot = nonebot.get_bot()
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=configs.guild_group_id,
                                 message=f'现在是{now.hour}点整~需要经验药水的小伙伴记得买药噢~')
    except:
        pass

@nonebot.scheduler.scheduled_job("cron", hour=0)
async def buy_potion_remind0():
    await send_potion_remind()

@nonebot.scheduler.scheduled_job("cron", hour=6)
async def buy_potion_remind6():
    await send_potion_remind()

@nonebot.scheduler.scheduled_job("cron", hour=12)
async def buy_potion_remind12():
    await send_potion_remind()

@nonebot.scheduler.scheduled_job("cron", hour=18)
async def buy_potion_remind18():
    await send_potion_remind()

@nonebot.scheduler.scheduled_job("cron", hour=14, minute=30)
async def jjcremind():
    bot = nonebot.get_bot()
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=configs.guild_group_id,
                                 message=f'现在是{now.hour}点{now.minute}分~每日背刺时间~')
    except:
        pass