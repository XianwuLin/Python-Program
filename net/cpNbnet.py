#!/usr/bin/env python
# coding:utf-8
import select
import socket

from nbNetUtils import DEBUG, dbgPrint

__all__ = ["nbNet"]


class STATE:
    def __init__(self):
        self.state = "accept"  # 定义状态
        self.have_read = 0  # 记录读了的字节
        self.need_read = 10  # 头文件需要读取10个字节
        self.have_write = 0  # 记录读了的字节
        self.need_write = 0  # 需要写的字节
        self.buff_read = ""  # 读缓存
        self.buff_write = ""  # 写缓存
        self.sock_obj = ""  # sock对象

    def printState(self):
        if DEBUG:
            dbgPrint('\n - current state of fd: %d' % self.sock_obj.fileno())
            dbgPrint(" - - state: %s" % self.state)
            dbgPrint(" - - have_read: %s" % self.have_read)
            dbgPrint(" - - need_read: %s" % self.need_read)
            dbgPrint(" - - have_write: %s" % self.have_write)
            dbgPrint(" - - need_write: %s" % self.need_write)
            dbgPrint(" - - buff_read: %s" % self.buff_read)
            dbgPrint(" - - buff_write: %s" % self.buff_write)
            dbgPrint(" - - sock_obj: %s" % self.sock_obj)


class nbNetBase:
    def setFd(self, sock):
        dbgPrint("\n setFd start")
        tmp_state = STATE()  # 实例化类
        tmp_state.sock_obj = sock  # 定义类中sock
        self.conn_state[sock.fileno()] = tmp_state  # 把sock加入到字典中
        self.conn_state[sock.fileno()].printState()
        dbgPrint("\n setFd end")

    def accept(self, fd):
        dbgPrint("\n accept start!")
        sock_state = self.conn_state[fd]  # 取出fd对应连接
        sock = sock_state.sock_obj  # 取出fd的sock
        conn, addr = sock.accept()  # 取出连接请求
        conn.setblocking(0)  # 设置非阻塞模式
        return conn  # 返回连接

    def close(self, fd):
        try:
            sock = self.conn_state[fd].sock_obj  # 取出fd的sock
            sock.close()  # 关闭sock
        except:
            dbgPrint("Close fd: %s" % fd)
        finally:
            self.epoll_sock.unregister(fd)  # 将fd重epoll中注销
            self.conn_state.pop(fd)  # 踢出字典

    def read(self, fd):
        try:
            sock_state = self.conn_state[fd]  # 取出fd对应连接
            conn = sock_state.sock_obj  # 取出fd连接请求
            if sock_state.need_read <= 0:  # 需要读取字节为空报错
                raise socket.error
            one_read = conn.recv(sock_state.need_read)  # 读取传输的字符
            dbgPrint("\n func fd: %d, one_read: %s, need_read: %d" %
                     (fd, one_read, sock_state.need_read))
            if len(one_read) == 0:  # 读取数据为0报错
                raise socket.error
            sock_state.buff_read += one_read  # 把读取数据存到读缓存中
            sock_state.have_read += len(one_read)  # 已经读取完的数据量
            sock_state.need_read -= len(one_read)  # 还需要读取数据的量
            sock_state.printState()
            if sock_state.have_read == 10:  # 10字节为头文件处理
                header_said_need_read = int(sock_state.have_read)  # 读取数据的量
                if header_said_need_read <= 0:  # 如果还需读0字节报错
                    raise socket.error
                sock_state.need_read += header_said_need_read  # 还需读取数量变化
                sock_state.buff_read = ''  # 读缓存清空
                sock_state.printState()
                return "readcontent"  # 还需读取数据
            elif sock_state.need_read == 0:
                return "process"  # 读取数据完成，转换状态
            else:
                return "readmore"  # 还需读取数据
        except (socket.error, ValueError), msg:
            try:
                if msg.errno == 11:  # errno等于11，尝试进行一次读取
                    dbgPrint("11" + msg)
                    return "retry"
            except:
                pass
            return "closing"

    def write(self, fd):
        sock_state = self.conn_state[fd]  # 取出fd对应的连接构造体
        conn = sock_state.sock_obj  # 取出fd对于连接
        last_have_send = sock_state.have_write  # 已经写数据的量
        try:
            have_send = conn.send(
                sock_state.buff_write[last_have_send:])  # 发送剩下的数据
            sock_state.have_write += have_send  # 已经写的数据量
            sock_state.need_write -= have_send  # 还需写的数据量
            if sock_state.need_write == 0 and sock_state.have_write != 0:  # 写数据完成
                sock_state.printState()
                dbgPrint("\n write date end")
                return "writecomplete"  # 返回写入完成
            else:
                return "writemore"  # 返回计算写入
        except socket.error, msg:
            return "closing"

    def run(self):
        while True:
            epoll_list = self.epoll_sock.poll()  # 定义poll()事件发生的list
            for fd, events in epoll_list:
                sock_state = self.conn_state[fd]  # 取出fd构造体
                if select.EPOLLHUP & events:  # 文件描述符挂断
                    dbgPrint("EPOLLHUP")
                    sock_state.state = "closing"  # fd状态设置为closing
                elif select.EPOLLERR & events:
                    dbgPrint("EPOLLERR")  # 文件描述符出错
                    sock_state.state = "closing"  # 对应fd状态为closing
                self.state_machine(fd)  # 状态机调用

    def state_machine(self, fd):
        sock_state = self.conn_state[fd]  # fd构造体
        self.sm[sock_state.state](fd)  # 通过sm字典调用对应状态的函数


class nbNet(nbNetBase):
    def __init__(self, addr, port, logic):
        dbgPrint('\n__init__: start!')
        self.conn_state = {}  # 定义字典保存每个连接状态
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.bind((addr, port))
        self.listen_sock.listen(10)  # 排队长度
        self.setFd(self.listen_sock)  # 定义listen socket 放入字典conn_state
        self.epoll_sock = select.epoll()  # 初始化fd的epoll
        self.epoll_sock.register(
            self.listen_sock.fileno(), select.EPOLLIN)  # linten可以读的描述符
        self.logic = logic  # 业务处理
        self.sm = {
            "accept": self.accept2read,
            "read": self.read2process,
            "write": self.write2read,
            "process": self.process,
            "closing": self.close,
        }  # 状态调用机的字典
        dbgPrint('\n__init__: end, register no: %s' %
                 self.listen_sock.fileno())

    def process(self, fd):
        sock_state = self.conn_state[fd]
        response = self.logic(sock_state.buff_read)  # 业务函数处理
        sock_state.buff_write = "%010d%s" % (len(response), response)  # 发送的数据
        sock_state.need_write = len(sock_state.buff_write)  # 需要发送的长度
        sock_state.state = "write"  # fd对应的状态
        self.epoll_sock.modify(fd, select.EPOLLOUT)  # fd对应的epoll为改写模式
        sock_state.printState()

    def accept2read(self, fd):
        conn = self.accept(fd)
        self.epoll_sock.register(
            conn.fileno(), select.EPOLLIN)  # 发送数据后重新将fd的epoll改成读
        self.setFd(conn)  # fd生成构造体
        self.conn_state[conn.fileno()].state = "read"  # fd状态为read
        dbgPrint("\n -- accept end!")

    def read2process(self, fd):
        read_ret = ""
        # 状态转换
        try:
            read_ret = self.read(fd)  # read函数返回值
        except (Exception), msg:
            dbgPrint(msg)
            read_ret = "closing"
        if read_ret == "process":  # 读取完成，转换到process
            self.process(fd)
        elif read_ret == "readcontent":  # readcontent、readmore、retry 继续读取
            pass
        elif read_ret == "readmore":
            pass
        elif read_ret == "retry":
            pass
        elif read_ret == "closing":
            self.conn_state[fd].state = 'closing'  # 状态为closing关闭连接
            self.state_machine(fd)
        else:
            raise Exception("impossible state returned by self.read")

    def write2read(self, fd):
        try:
            write_ret = self.write(fd)  # 函数write返回值
        except socket.error, msg:  # 出错关闭连接
            write_ret = "closing"
        if write_ret == "writemore":  # 继续写
            pass
        elif write_ret == "writecomplete":  # 写完成
            sock_state = self.conn_state[fd]
            conn = sock_state.sock_obj
            self.setFd(conn)  # 重置见连接fd构造体
            self.conn_state[fd].state = "read"  # 将fd状态设置为read
            self.epoll_sock.modify(fd, select.EPOLLIN)  # epoll状态为可读
        elif write_ret == "closing":  # 发生错误关闭
            dbgPrint(msg)
            self.conn_state[fd].state = 'closing'
            self.state_machine(fd)


if __name__ == '__main__':
    def logic(d_in):
        return(d_in[::-1])
    reverseD = nbNet('0.0.0.0', 9060, logic)
    reverseD.run()
