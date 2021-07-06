import socket
import struct
import cv2
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 6666))

cap = cv2.VideoCapture(0)

# 图片进行压缩的参数
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue
    # 将图片进行压缩
    result,frame_encode = cv2.imencode('.jpg', frame, encode_param)
    # 将图片转化成bytes字节对象
    frame_bytes = pickle.dumps(frame_encode, 0)
    # 获取图片字节的长度
    size = len(frame_bytes)
    # 将长度进行编码
    size = struct.pack('L', size)
    # 将图片长度和图片发送给服务器
    client_socket.sendall(size + frame_bytes)
