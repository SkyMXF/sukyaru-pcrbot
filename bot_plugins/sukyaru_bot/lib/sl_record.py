from user.models import UserInfo

def set_sl(user_qq):

    try:
        user_info = UserInfo.objects.get(user_qq_id=user_qq)
    except:
        return False, "记录失败：凯露酱这里没有你的qq的记录噢"
    
    if user_info.user_add_type == 1:
        return False, "无法记录SL: 骑士君'%s'今天已经使用过SL了噢"%(user_info.nickname)
    else:
        user_info.user_add_type = 1
        user_info.save()
        return True, "骑士君'%s', SL已记录"%(user_info.nickname)

def reset_all_sl():

    user_info_set = UserInfo.objects.all()
    for user_info in user_info_set:
        user_info.user_add_type = 0
        user_info.save()