from socket import *
import random, sys
import signal
from multiprocessing import Process
import os
from select import select

msg = "C 01 01 13 xx "
msg1 = "出牌者,对象,花色，牌名"

HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)
Player_info = {'user_name': 'pwd'}  # 玩家信息库
player_id_dic = {'房间号': {'身份': 'connfd'}}  # {'房间号':{'身份': 'connfd'}} 玩家房间号映射身份字典
connfd_list = []  # 玩家套接字列表

print(Player_info)
print(player_id_dic)

# 测试数据
poker_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
identity_list = ['反贼', '主公', '反贼', '忠臣', '奸细']


# 用户注册与登录
class R_D():
    def __init__(self):
        pass

    # 处理用户注册账号
    def do_register(self, name, pwd, connfd):
        if name in player_id_dic.keys():
            connfd.send("用户名已存在".encode())
        Player_info[name] = pwd
        connfd.send(b"OK")

    # 处理用户登陆
    def do_login(self, name, pwd, connfd):
        if name in Player_info.keys() and Player_info[name] == pwd:
            connfd.send(b"OK")
            connfd_list.append(connfd)
        elif name in Player_info.keys() and Player_info[name] != pwd:
            connfd.send("密码错误".encode())
        else:
            connfd.send("用户名不存在".encode())
        return


# 洗牌方法
def shuffle(target_list):
    random.shuffle(target_list)
    return


def mk_room(connfd):
    data = connfd.recv(100).decode()
    if data in player_id_dic.keys():
        connfd.send("该房间号已存在".encode())
    player_id_dic[data][connfd] = 0  # ccccccccccccccccccccccccc
    print(player_id_dic)  # ccccccccccccccccccccccccc
    msg = '创建成功，您的房间号是：%s' % data
    connfd.send(msg.encode())


def chose_room(connfd):
    data = connfd.recv(100).decode()
    if data not in player_id_dic.keys():
        connfd.send("该房间号不存在".encode())
    player_id_dic[data][connfd] = 0  # ccccccccccccccccccccccccccc
    print(player_id_dic)  # ccccccccccccccccccccccccc
    msg = '欢迎来到%s号房间' % data
    connfd.send(msg.encode())


def do_request(connfd):
    rd = R_D()
    while True:
        data = connfd.recv(1024)
        if data.decode().split(" ")[0] == "R":
            name = data.decode().split(" ")[1]
            pwd = data.decode().split(" ")[2]
            rd.do_register(name, pwd, connfd)  # 注册操作
            print(Player_info)
        elif data.decode().split(" ")[0] == "L":
            name = data.decode().split(" ")[1]
            pwd = data.decode().split(" ")[2]
            rd.do_login(name, pwd, connfd)  # 登陆操作
            print(player_id_dic)
        elif data.decode() == '#':
            print("%s已断开连接" % connfd)


class Game():
    def __init__(self):
        game_start(room_id, connfd)

    def game_start(self, room_id, connfd):
        for connfd in player_id_dic[room_id].keys():
            shenfen(identity_list, poker_list, room_id, connfd)

            # 开始游戏

    # 发牌方法
    def fapai(self, poker_list):
        # shuffle(poker_list)  # 洗牌
        p = " "
        # list01=[]
        # list01[:]=poker_list[0:4]
        # return " ".join(list01)
        # del poker_list[0:4]
        for i in range(4):
            p += "%s " % poker_list.pop()
        return p

    # 给玩家分配身份并发牌
    def shenfen(self, identity_list, poker_list, room_num, connfd):
        for target_connfd in connfd_list:
            identity = identity_list.pop()
            player_id_dic[room_num][target_connfd] = identity#cccccccccccccccccccc
            print(player_id_dic)  # ccccccccccccccccccccccccc
            p = fapai(poker_list)
            msg = p + identity
            connfd.send(msg.encode())
        return


# 网络搭建
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(10)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务区退出")
        except Exception as e:
            print(e)
            continue
        print("Connect from", addr)

        # # 创建线程
        # p1 = Process(do_request(connfd))
        # p1.start()
        # p1.join()




        # 创建子进程
        pid = os.fork()
        if pid < 0:
            pass
        elif pid == 0:
            sockfd.close()
            do_request(connfd)
            os._exit(0)
        else:
            connfd.close()

        # 遍历寻找满5人的房间，并开始游戏
        for room_id in player_id_dic.keys():
            if len(player_id_dic[room_id]) == 5:
                # rlist = [connfd]
                wlist = []
                xlist = []
                # select IO多路复用
                while True:
                    try:
                        rs, ws, xs = select(player_id_dic[room_id].values(), wlist, xlist)
                    except KeyboardInterrupt:
                        print('server退出')
                        break

                    a=Game(room_id, connfd)  # r是connfd


if __name__ == "__main__":
    main()
