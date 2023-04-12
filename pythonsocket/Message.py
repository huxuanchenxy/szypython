import struct
 
# 注册消息ID
MSG_ID_REGISTER = 0x00
# 心跳消息ID
MSG_ID_HEARTBEAT = 0x01
# 时间消息ID
MSG_ID_DATETIME = 0x02
 
 
def pack(fmt, *args):
    args_list = list(args)
    for i, arg in enumerate(args_list):
        if isinstance(arg, str):
            args_list[i] = arg.encode('utf-8')
    return struct.pack(fmt, *args_list)
 
 
# 组装注册消息
def msg_register(appid, imei):
    return pack('!b36s15s', MSG_ID_REGISTER, appid, imei)
 
 
# 组装心跳消息
def msg_heartbeat():
    return pack('!b', MSG_ID_HEARTBEAT)
 
 
# 组装时间消息
def msg_datetime():
    return pack('!b', MSG_ID_DATETIME)