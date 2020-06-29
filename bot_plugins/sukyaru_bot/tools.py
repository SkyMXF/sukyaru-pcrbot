from nonebot import on_command, CommandSession, scheduler
import nonebot
from apscheduler.triggers.date import DateTrigger

import pytz
import datetime
import re

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
    
@on_command('clock', aliases=("计时"))
async def clock(session: CommandSession):
    print(session.state["valid_cmd"])
    print(session.state["hour"], session.state["minute"], session.state["second"], session.state["text"])
    return
    await session.send('收到~凯露酱会在8小时后提醒你~')

    # 创建触发器
    delta = datetime.timedelta(hours=8)
    trigger = DateTrigger(
        run_date=datetime.datetime.now() + delta
    )

    # 添加任务
    scheduler.add_job(
        func=session.send,  # 要添加任务的函数，不要带参数
        trigger=trigger,  # 触发器
        args=('不要再赖床啦！',),  # 函数的参数列表，注意：只有一个值时，不能省略末尾的逗号
        # kwargs=None,
        misfire_grace_time=60,  # 允许的误差时间，建议不要省略
        # jobstore='default',  # 任务储存库，在下一小节中说明
    )

@clock.args_parser
async def clock_parser(session: CommandSession):
    
    arg_text = session.current_arg_text.strip()

    arg_re = re.compile(r"(?P<hour>\d+)(?:\.(?P<minute>\d+))?(?:\.(?P<second>\d+))?(?:\s+(?P<text>.*))?")
    match_args = re.search(arg_re, arg_text)

    if match_args:
        # 格式正确
        session.state["valid_cmd"] = True   # 有效指令

        session.state["hour"] = match_args.group("hour")
        session.state["minute"] = match_args.group("minute")
        session.state["second"] = match_args.group("second")
        session.state["text"] = match_args.group("text")
    else:
        session.state["valid_cmd"] = False
