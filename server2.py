from socket import *
import random, sys
import signal
import json,time
from multiprocessing import Process
import os
from select import select

HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)
Player_info = {'user_name': 'pwd', 'aa': '123'}  # 玩家信息库
# player_id_dic = {'房间号': {'connfd': '身份'}}  # {'房间号':{'connfd':'身份' }} 玩家房间号映射身份字典
room_dic = {'房间号': {'connfd': '身份'}}  # {'房间号': {'connfd':'身份',...}} 玩家房间号映射身份字典
connfd_list = []  # 玩家套接字列表

print(Player_info)
print(room_dic)

# 测试数据
poker_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
identity_list = ['反贼', '主公', '反贼', '忠臣', '内奸']


# 洗牌方法
def shuffle(target_list):
    random.shuffle(target_list)
    return


# 用户注册、登录、选择要进入的进入房间
class R_D():
    def __init__(self, connfd):
        self.connfd = connfd

    # 处理用户注册账号
    def do_register(self, name, pwd):
        if name in Player_info.keys():
            self.connfd.send("用户名已存在".encode())
        Player_info[name] = pwd
        self.connfd.send(b"OK")

    # 处理用户登陆
    def do_login(self, name, pwd):
        if name in Player_info.keys() and Player_info[name] == pwd:
            self.connfd.send(b"OK")
            connfd_list.append(self.connfd)
        elif name in Player_info.keys() and Player_info[name] != pwd:
            self.connfd.send("密码错误".encode())
        else:
            self.connfd.send("用户名不存在".encode())
        return

    # 创建房间
    def mk_room(self, room_id):
        room_dic[room_id] = {self.connfd: None}  # 默认身份为None，后面添加 cccccccccccccccccccc
        print(room_dic)  # 测试房间字典是否添加用户信息ccccccccccccccccccccccccc
        msg = '您输入的房间号不存在，自动为您创建并进入房间，您所在的房间号是：%s' % room_id
        self.connfd.send(msg.encode())

    # 选择房间
    def chose_room(self, room_id, rlist):
        print('进入选择房间方法')  # 测试
        for i in room_dic.keys():
            print(i)
        if room_id not in room_dic.keys():  # 如果房间号不存在，则创建新的房间
            self.mk_room(room_id)
            return
        elif len(room_dic[room_id]) == 2:
            self.connfd.send("该房间已满".encode())
            return
        room_dic[room_id][self.connfd] = None  # 默认身份为None，后面添加ccccccccccccccccccccccccccc
        print(room_dic)  # 测试房间字典是否添加用户信息ccccccccccccccccccccccccc
        msg = '欢迎来到%s号房间' % room_id
        self.connfd.send(msg.encode())
        # rlist.remove(self.connfd)


# 处理请求（注册、登录、选房间）
def do_request(connfd, rlist):
    try:
        data1 = connfd.recv(1024)
    except Exception as e:
        print(e)
        return
    data = data1.decode().split(" ")
    key = data[0]
    # 创建R_D（登录、注册类）对象
    rd = R_D(connfd)
    # 处理请求
    if key == "R":
        name = data[1]
        pwd = data[2]
        rd.do_register(name, pwd)  # 注册操作
        print(Player_info)
    elif key == "L":
        name = data[1]
        pwd = data[2]
        rd.do_login(name, pwd)  # 登陆操作
        print(room_dic)
    elif key == 'CHO':
        room_id = data[1]
        rd.chose_room(room_id, rlist)  # 选择房间
        time.sleep(1)
        if len(room_dic[room_id]) == 2:
            g = Game(room_id)
            g.game_start()
        # msg = '房间当前人数为%s' % len(room_dic[room_id])
        # connfd.send(msg.encode())
    elif key == '#':
        print("%s已退出" % str(connfd).split('),')[1])


# 启动服务器
def server_start():
    sockfd = socket(AF_INET, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(10)
    rlist = [sockfd]
    wlist = []
    xlist = []
    # select IO多路复用
    while True:
        try:
            rs, ws, xs = select(rlist, wlist, xlist)
        except KeyboardInterrupt:
            print('server退出')
            break
        for r in rs:
            if r is sockfd:
                connfd, addr = r.accept()
                print(addr)
                rlist.append(connfd)
            else:
                do_request(r, rlist)


# 初始化玩家身份和手牌
class Game():
    def __init__(self, room_id):
        self.room_id = room_id

    # 给玩家分配身份
    def send_identity_and_inti_poker(self):
        shuffle(identity_list)  # 洗牌（身份牌）
        for target_connfd in connfd_list:
            identity = identity_list.pop()
            room_dic[self.room_id][target_connfd] = identity  # 将身份添加到room_dic字典 cccccccccccccccccccc
            print(room_dic)  # 测试身份是否加入ccccccccccccccccccccccccc
            target_connfd.send(identity.encode())
            init_poker_list = self.init_pofer()
            msg = json.dumps(init_poker_list)
            target_connfd.send(msg.encode())
        return

    # 初始化手牌+身份
    def init_pofer(self):
        shuffle(poker_list)  # 洗牌
        init_poker_list = []
        init_poker_list[:] = poker_list[0:4]
        del poker_list[0:4]
        return init_poker_list

    def game_start(self):
        self.send_identity_and_inti_poker()
        # 开始游戏
        print("等待获取玩家的出牌.....")




def second_process():
    # select IO多路复用
    # rlist = []
    wlist = []
    xlist = []

    while True:
        for room_id in room_dic.keys():
            try:
                rs, ws, xs = select(room_dic[room_id].keys(), wlist, xlist)  # 监控每一个房间的套接字对象，如有活跃则执行后面的代码
            except KeyboardInterrupt:
                sys.exit('server退出')
            except Exception as e:
                print(e)
                sys.exit('游戏层进程异常退出')
            for connfd in rs:
                data = connfd.recv(1024).decode()
                print(data)  # 测试


def main():
    # 启动服务器
    server_start()

    # second_process()


if __name__ == "__main__":
    main()
