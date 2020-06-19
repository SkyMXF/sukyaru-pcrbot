from nonebot import on_command, CommandSession
import nonebot

from .lib import configs, user_register
import bot_config

@on_command(name="register", aliases=("注册"))
async def register(session: CommandSession):
    # args：
    # qq
    # nickname
    # auth -暂不需要，默认为2(普通群员)

    success, message = user_register.register_user(
        user_info_dict={
            "user_qq": int(session.state["user_qq"]),
            "password": configs.reg_default_pwd,
            "nickname": session.state["nickname"],
            "user_auth": 2
        }
    )

    await session.send(
        "%s"%(message)
    )

@register.args_parser
async def register_parser(session: CommandSession):
    #arg_text = session.current_arg_text.strip()

    session.state["user_qq"] = session.event.sender["user_id"]
    session.state["nickname"] = session.event.sender["nickname"]

@on_command(name="guild_register", aliases=("公会注册"))
async def guild_register(session: CommandSession):
    # args：
    # qq
    # nickname
    # auth -暂不需要，默认为2(普通群员)

    # 获取成员列表
    bot = nonebot.get_bot()
    group_member_list = await bot.get_group_member_list(group_id=bot_config.PCR_group_id)
    failed_list = []
    for member_info in group_member_list:
        # 逐一注册成员
        success, message = user_register.register_user(
        user_info_dict={
            "user_qq": member_info["user_id"],
            "password": configs.reg_default_pwd,
            "nickname": member_info["card"],
            "user_auth": 2
        }
        if not success:
            failed_list.append((member_info["user_id"], member_info["card"]))
    )

    await session.send(
        "公会注册完成，失败成员列表：%s"%(str(failed_list))
    )

@guild_register.args_parser
async def guild_register_parser(session: CommandSession):
    pass