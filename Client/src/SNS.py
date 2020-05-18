import os
#获取当前用户列表
def get_info():
    SNS_List = {
        'QQ' : [],
        'Wechat': [],
        'WangWang': [],
        'error':'no'
    }
    try:
        users_path = r"C:\Users"
        user_list = os.listdir(users_path)
        remove_list = ['All Users','Default','Default User','desktop.ini','Public','Applet','All Users','system']
        wwpath_list = [r':\Program Files (x86)\AliWangWang\profiles',r'\Program Files\AliWangWang\profiles']
        disk_list = ['C','D','E','F','E','H']
        for r_item in remove_list:
            if r_item in user_list:
                user_list.remove(r_item)
        for user in user_list:
            t_path = users_path + r'\{}\Documents\Tencent Files'.format(user)
            if os.path.exists(t_path):
                SNS_List['QQ'] = os.listdir(t_path)
                for r_item in remove_list:
                    if r_item in SNS_List['QQ']:
                        SNS_List['QQ'].remove(r_item)
            w_path = users_path + r'\{}\Documents\WeChat Files'.format(user)
            if os.path.exists(w_path):
                SNS_List['Wechat'] = os.listdir(w_path)
                for r_item in remove_list:
                    if r_item in SNS_List['Wechat']:
                        SNS_List['Wechat'].remove(r_item)
            for disk_item in disk_list:
                for wwpath_item in wwpath_list:
                    path = disk_item + wwpath_item
                    if os.path.exists(path):
                        SNS_List['WangWang'] = os.listdir(path)
                        for r_item in remove_list:
                            if r_item in SNS_List['WangWang']:
                                SNS_List['WangWang'].remove(r_item)
                        break
        return SNS_List
    except Exception as e:
        SNS_List['error'] = str(e)
        return SNS_List