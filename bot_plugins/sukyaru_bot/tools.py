from nonebot import on_command, CommandSession
import nonebot

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