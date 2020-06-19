from nonebot import on_command, CommandSession

# on_command为装饰器，可将函数声明为命令处理器
@on_command(name="weather", aliases=("天气", "天气预报"))   # 命令名称及别名
async def weather(session: CommandSession):
    city = session.get("city", prompt="哪个城市？")     # 获取命令内容
    weather_report = await get_weather_of_city(city)
    await session.send(weather_report)                  # 发送

# weather.args_parser将函数装饰为weather命令的argparser
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state["city"] = stripped_arg
        return
    
    if not stripped_arg:
        session.pause("没有输入城市")

    session.state[session.current_key] = stripped_arg

async def get_weather_of_city(city: str):
    return "%s的天气是大晴天~"%city