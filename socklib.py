import socket
import struct
import pickle
# only argument for the struct is major version, minor version, length
HEADER_FORMAT = "!HHQ"
MAJOR_VERSION = 2
MINOR_VERSION = 0
HEADER_BYTESIZE = struct.calcsize(HEADER_FORMAT)
ERR_WRONG_VERSION = -1
ERR_EOF = -2

def encode_msg(msg):
    msg = pickle.dumps(msg)
    msg_len = len(msg)
    header = struct.pack(HEADER_FORMAT,MAJOR_VERSION,MINOR_VERSION,msg_len)
    return header + msg

def recv_msg(sock: socket.socket):
    header_bytes = sock.recv(HEADER_BYTESIZE,socket.MSG_WAITALL)
    if not header_bytes:
        return ERR_EOF
    major_version,minor_version,msg_len = struct.unpack(HEADER_FORMAT,header_bytes)
    if (major_version != MAJOR_VERSION or minor_version != MINOR_VERSION):
        return ERR_WRONG_VERSION
    msg_bytes = sock.recv(msg_len,socket.MSG_WAITALL)
    msg = pickle.loads(msg_bytes,fix_imports=True)
    return msg
    