from nonebot import on_command, CommandSession

from .lib import configs, user_register

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
    