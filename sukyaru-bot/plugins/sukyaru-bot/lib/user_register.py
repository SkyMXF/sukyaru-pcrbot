from .....sukyaru-web.user.models import UserInfo
from .....sukyaru-web.main import utils

def register_user(user_info_dict):
    # dict需要: "user_qq", "password", "nickname", "user_auth"
    # 返回：success(true/false), message 
    
    # 查看是否已注册
    find_user = UserInfo.objects.filter(user_qq_id=user_info_dict["user_qq"])
    if len(find_user) > 0:
        return False, "该qq已注册，如果忘记密码可以发送'重置密码'将密码重置"
    
    try:
        UserInfo.objects.create(
            user_qq_id=user_info_dict["user_qq"],
            password=utils.pwd_hash(user_info_dict["password"]),
            nickname=user_info_dict["nickname"],
            user_auth=user_info_dict["user_auth"],
            user_add_type=0
        )
    except Exception as e:
        return False, str(e)
    
    return True, "注册成功, 初始密码为%s"%(user_info_dict["password"])