from client2 import *
import sys, json, time
from socket import *
from select import select

# 创建套接字对象
sockfd = socket(AF_INET, SOCK_STREAM)
try:
    sockfd.connect(ADDR)
except KeyboardInterrupt:
    sockfd.close()
    sys.exit('主动退出')
except Exception as e:
    print(e)
    sys.exit("连接服务器失败，客户端退出")

# 创建对象调用功能函数
rd = R_D(sockfd)


def main():
    while True:

        print('*****************************')
        print('  1.注册    2. 登陆   3.退出  ')
        print('*****************************')
        try:
            msg = input("请选择您的操作：")
        except KeyboardInterrupt:
            msg = '# %s' % ("退出")  # 客户端断开或退出协议
            sockfd.send(msg.encode())
            sockfd.close()
            sys.exit('主动退出')
        if msg == "1":
            rd.do_register()  # 登录
        elif msg == "2":
            rd.do_login()  # 注册
            erji()
        elif msg == "3":  # 退出
            rd.do_exit()


# 二级界面
def erji():
    while True:
        print('******************************************')
        print('       1.进入房间         2.退出          ')
        print('*****************************************')
        msg = input("请输入选项：")
        if msg == "1":
            rd.chose_room()
            game_start()
        elif msg == "2":
            break


# 循环打印三级界面
def sanji(data):
    print('******************************************')
    print('**                                      **')
    print('**                                      **')
    print('     %s' % data)
    print('**                                      **')
    print('**                                      **')
    print('*****************************************')


# 三级界面数据处理
def game_start():
    while True:
        data = sockfd.recv(1024).decode()
        if not data:
            sys.exit('服务器异常退出')
        sanji(data)


if __name__ == '__main__':
    main()
