from client2 import *
import sys

sockfd = socket()
try:
    sockfd.connect(ADDR)
except KeyboardInterrupt:
    sockfd.close()
    sys.exit('sdfsf')
except Exception as e:
    print(e)
    sys.exit("连接服务器失败，客户端退出")


def main():

    # 创建对象调用功能函数
    rd = R_D(sockfd)
    while True:

        print('*****************************')
        print('  1.注册    2. 登陆   3.退出  ')
        print('*****************************')
        try:
            msg = input("请选择您的操作：")
        except KeyboardInterrupt:
            msg=b'#'#客户端断开或退出协议
            sockfd.send(msg)
            sockfd.close()
            sys.exit('客户端退出')
        if msg == "1":
            rd.do_register()
        elif msg == "2":
            rd.do_login()
            erji()
        elif msg == "3":
            do_exit(sockfd)

def erji():
    while True:
        print('******************************************')
        print('  1.创建房间   2. 选择进入已有房间   3.退出  ')
        print('*****************************************')
        msg = input("请输入选项：")
        if msg == "1":
            pass
        elif msg == "2":
            pass
            chose_room(sockfd)
        elif msg == "3":
            break


if __name__ == '__main__':
    main()
