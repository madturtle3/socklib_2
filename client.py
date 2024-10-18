import socket
import chatlib
import socklib


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(("",chatlib.PORT))
sock.send(socklib.encode_msg(chatlib.InitMsg("john")))
sock.send(socklib.encode_msg(chatlib.ChatMsg(None,"hello!")))
sock.close()