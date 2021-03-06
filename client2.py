﻿import getpass, sys, json

HOST = "127.0.0.1"
PORT = 8000
ADDR = (HOST, PORT)

poker_dic = {"0": "手牌"}  # 手牌库


class R_D():
    def __init__(self, sockfd):
        self.sockfd = sockfd

    # 注册账号
    def do_register(self):
        while True:
            user_name = input("用户名：")
            pwd = getpass.getpass("用户名密码：")
            pwd1 = getpass.getpass("确认密码：")
            if pwd != pwd1:
                print("两次密码不一致!")
                continue
            elif (" " in user_name) or (" " in pwd):
                print("用户名和密码不能有空格")
                continue
            msg = "R %s %s" % (user_name, pwd)
            # 发送注册请求
            self.sockfd.send(msg.encode())
            # 等待回复
            data = self.sockfd.recv(1024)
            if data.decode() == "OK":
                print("注册成功")
            else:
                print("注册失败", data.decode())
            return

    # 登陆
    def do_login(self):
        while True:
            user_name = input("用户名：")
            pwd = getpass.getpass("用户名密码：")
            msg = "L %s %s" % (user_name, pwd)
            # 发送登陆请求
            self.sockfd.send(msg.encode())
            # 等待回复
            data = self.sockfd.recv(1024)
            if data.decode() == 'OK':
                print("登陆成功")
                return
            else:
                print("登陆失败", data.decode())
                continue

    def chose_room(self):
        while True:
            room_id = input("请输入房间号：")
            msg = "CHO %s" % room_id
            self.sockfd.send(msg.encode())
            data = self.sockfd.recv(1024).decode()
            if data == '该房间已满':
                print(data)
                continue
            print(data)
            return

    def do_exit(self):
        self.sockfd.send(b'#')
        self.sockfd.close()
        sys.exit('退出客户端')

    # 开始游戏
    # def game_start(self):
    #     data = self.sockfd.recv()  # 获取身
    #     identity = data.decode().split(" ")[0]  # 身份
    #     poker_list = data.decode().split(" ")[1]  # 手牌字符串
    #     print(identity)
    #     print(poker_dic)
    #
    #     # 手牌编号
    #     count = 1
    #     # 将手牌存入玩家手牌字典库
    #     for poker in poker_list:
    #         poker_dic[count] = poker
    #         count += 1
    #
    #     # 游戏，接收和发送数据
    #     while True:
    #         data, addr = sockfd.recvfrom(1024)
    #         print(data.decode())
    #         while True:
    #             num = input("请输入你要出的手牌序号：")
    #             if num not in poker_dic.keys():
    #                 print("您输入的序号有误!")
    #                 continue
    #             sockfd.sendto(poker_dic[num].encode(), ADDR)
    #             # break

    # 获取身份和初始化手牌


    def get_identity_and_inti_poker(self):
        identity = self.sockfd.recv(1024).decode()
        print("您的身份为：%s" % identity)
        init_popker = self.sockfd.recv(1024).decode()
        msg = json.load(init_popker)
        print("您的初始手牌为：%s" % msg)
        print("等待玩家出牌...")
