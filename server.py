import socket
import struct
import cv2
import pickle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 6666))
server_socket.listen(5)
client_socket, addr = server_socket.accept()

# 用于不断接受客户端传输的数据
data = b''
# 数据长度编码后的长度，比如说用于存放的数据占用几个字节
length = struct.calcsize('L')
while True:
    # 先接受传输图片的长度
    if len(data) < length:
        data += client_socket.recv(4096)
    # 获取图片的长度字节
    size = data[:length]
    # 图片字节数据
    data = data[length:]
    # 获取图片的长度
    data_len = struct.unpack('L', size)[0]
    # 如果接受的字节长度小于图片长度,进行不断的接受
    while len(data) < data_len:
        data += client_socket.recv(4096)
    # 拿出该图片长度的字节数据
    frame = data[:data_len]
    # 将剩下的数据保存到下一次接受
    data = data[data_len:]
    # 将图片解码为array
    frame = pickle.loads(frame, fix_imports=True, encoding='bytes')
    # 将图片解压缩
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('', frame)
    cv2.waitKey(1)
