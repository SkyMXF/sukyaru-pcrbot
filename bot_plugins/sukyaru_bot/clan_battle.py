from nonebot import on_command, CommandSession
import nonebot

import datetime
import re

from .lib import configs, battle_report
import bot_config

@on_command(name="report", aliases=("报刀"))
async def report(session: CommandSession):
    # args：
    # qq
    # nickname
    # auth -暂不需要，默认为2(普通群员)
    await session.send(session.state["test_field"])
    return

    success, message = battle_report.report(
        battle_record_dict={
            "user_qq": session.state["user_qq"],
            "boss_real_stage": session.state["boss_real_stage"],
            "boss_id": session.state["boss_id"],
            "damage": session.state["damage"],
            "record_date": session.state["record_date"],
            "final_kill": session.state["final_kill"],
            "comp_flag": session.state["comp_flag"]
        }
    )

    await session.send(
        "%s"%(message)
    )

report_example = "报刀 1-1 876543 或 报刀 1-1 54321 补偿"

@report.args_parser
async def report_parser(session: CommandSession):
    arg_text = session.current_arg_text.strip()

    arg_re = re.compile(r"\s*(?P<boss_real_stage>\d+)\-(?P<boss_id>\d+)\s+(?P<damage>\d+)\s*(?P<comp_flag>补偿)?\s*")
    match_args = re.search(arg_re, arg_text)

    session.state["test_field"] = "stage %s, boss_id %s, damage %s, comp_flag %s"%(
        match_args.group("boss_real_stage"),
        match_args.group("boss_id"),
        match_args.group("damage"),
        match_args.group("comp_flag"),
    )
    return

    now_datetime = datetime.datetime.utcnow()
    session.state["user_qq"] = session.event.sender["user_id"]
    session.state["record_date"] = now_datetime
