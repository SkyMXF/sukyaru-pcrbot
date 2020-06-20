from nonebot import on_command, CommandSession
import nonebot

import datetime
import re

from .lib import configs, battle_report, sl_record
import bot_config

report_example = "报刀 1-1 876543 或 报刀 1-1 54321 补偿"

@on_command(name="report", aliases=("报刀"), only_to_me=False)
async def report(session: CommandSession):
    
    if not session.state["valid_report"]:
        await session.send("报刀格式有误噢~示例：%s"%(report_example))
        return

    # 输入格式检查
    try:
        session.state["user_qq"] = int(session.state["user_qq"])
        session.state["boss_real_stage"] = int(session.state["boss_real_stage"])
        session.state["boss_id"] = int(session.state["boss_id"])
        session.state["damage"] = int(session.state["damage"])
        session.state["operator_qq"] = int(session.state["operator_qq"])
    except Exception as e:
        print(e)
        await session.send("报刀格式有误噢~示例：%s"%(report_example))

    success, message = battle_report.report(
        battle_record_dict={
            "user_qq": session.state["user_qq"],
            "boss_real_stage": session.state["boss_real_stage"],
            "boss_id": session.state["boss_id"],
            "damage": session.state["damage"],
            "record_date": session.state["record_date"],
            "final_kill": session.state["final_kill"],
            "comp_flag": session.state["comp_flag"],
            "operator_qq": session.state["operator_qq"]
        }
    )

    await session.send(
        "%s"%(message)
    )

@report.args_parser
async def report_parser(session: CommandSession):
    arg_text = session.current_arg_text.strip()

    arg_re = re.compile(r"\s*(?P<boss_real_stage>\d+)\-(?P<boss_id>\d+)\s+(?P<damage>\d+)\s*(?P<comp_flag>补偿)?\s*(?:qq=)?(?P<record_qq>\d+)?\s*")
    match_args = re.search(arg_re, arg_text)

    if match_args:
        # 格式正确
        session.state["valid_report"] = True    # 有效报刀

        now_datetime = datetime.datetime.now()

        session.state["user_qq"] = session.event.sender["user_id"] if match_args.group("record_qq") is None else match_args.group("record_qq")
        session.state["operator_qq"] = session.event.sender["user_id"]
        session.state["boss_real_stage"] = match_args.group("boss_real_stage")
        session.state["boss_id"] = match_args.group("boss_id")
        session.state["damage"] = match_args.group("damage")
        session.state["record_date"] = now_datetime
        session.state["final_kill"] = False     # 暂不使用
        session.state["comp_flag"] = False if match_args.group("comp_flag") != "补偿" else True
    else:
        session.state["valid_report"] = False

redo_example = "撤销记录 10"

@on_command(name="redo_report", aliases=("撤销记录"))
async def redo_report(session: CommandSession):
    
    if not session.state["valid_report"]:
        await session.send("指令格式有误噢~示例：%s"%(redo_example))
        return

    # 输入格式检查
    try:
        session.state["record_id"] = int(session.state["record_id"])
        session.state["operator_qq"] = int(session.state["operator_qq"])
    except Exception as e:
        print(e)
        await session.send("指令格式有误噢~示例：%s"%(redo_example))

    success, message = battle_report.redo(
        record_id=session.state["record_id"],
        operator_qq=session.state["operator_qq"]
    )

    await session.send(
        "%s"%(message)
    )

@redo_report.args_parser
async def redo_report_parser(session: CommandSession):
    arg_text = session.current_arg_text.strip()

    arg_re = re.compile(r"\s*(?P<record_id>\d+)\s*")
    match_args = re.search(arg_re, arg_text)

    if match_args:
        # 格式正确
        session.state["valid_report"] = True    # 有效指令

        session.state["operator_qq"] = session.event.sender["user_id"]
        session.state["record_id"] = match_args.group("record_id")
        
    else:
        session.state["valid_report"] = False

@on_command(name="SL", aliases=("SL", "sl"))
async def battle_sl(session: CommandSession):

    # 输入格式检查
    try:
        session.state["user_qq"] = int(session.state["user_qq"])
    except Exception as e:
        print(e)
        await session.send("异常：传输的QQ不是数字")

    success, message = sl_record(session.state["user_qq"])

    await session.send(
        "%s"%(message)
    )

@battle_sl.args_parser
async def battle_sl_parser(session: CommandSession):
    session.state["user_qq"] = session.event.sender["user_id"]

@nonebot.scheduler.scheduled_job("cron", hour=5)
async def reset_every_member_sl():
    sl_record.reset_all_sl()