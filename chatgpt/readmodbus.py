import struct
import binascii

# bytes = b'\x43\xEF\xA0\xFE'
# float_value = struct.unpack('>f', bytes)[0]

# print(float_value)



# hex_string = "68 65 61 72 74 3D 6F 6B 0A"
# byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
# ascii_string = byte_string.decode("ascii")

# print("11",ascii_string,"22")






# hex_string = "69 6D 65 69 3D 33 35 35 39 35 32 30 39 36 35 30 32 31 36 39 3B 63 63 69 64 3D 38 39 38 36 30 34 41 33 31 39 32 31 43 31 39 31 33 38 38 32 3B 76 65 72 73 3D 31 2E 30 3B 74 79 70 65 3D 31 33 35 3B 6E 68 33 3D 31 31 2E 37 33 3B 68 32 73 3D 38 2E 31 36 3B 72 73 73 69 3D 31 35 3B 73 6E 72 3D 31 33 3B 63 6F 75 6E 74 3D 31 33 0A"
# byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
# ascii_string = byte_string.decode("ascii")

# print("11",ascii_string,"22")


# hex_string = "63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A"
# byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
# ascii_string = byte_string.decode("ascii")

# print("11",ascii_string,"22")

# hex_string = "63 6F 6E 6E 65 63 74 3D 6F 6B 0A"
# byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
# ascii_string = byte_string.decode("ascii")

# print("11",ascii_string,"22")


# hex_string = "69 6D 65 69 3D 33 35 35 39 35 32 30 39 36 35 30 39 38 34 32 3B 63 63 69 64 3D 38 39 38 36 30 34 41 33 31 39 32 31 43 31 39 31 33 39 31 39 3B 76 65 72 73 3D 31 2E 30 3B 74 79 70 65 3D 31 33 35 3B 6E 68 33 3D 31 31 2E 36 37 3B 68 32 73 3D 31 30 2E 38 38 3B 72 73 73 69 3D 31 31 3B 73 6E 72 3D 31 37 3B 63 6F 75 6E 74 3D 31 38 35 37 0A"
# byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
# ascii_string = byte_string.decode("ascii")

# print("333",ascii_string,"444")


# hex_string = "69 6D 65 69 3D 33 35 35 39 35 32 30 39 36 35 30 39 38 34 32 3B 63 63 69 64 3D 38 39 38 36 30 34 41 33 31 39 32 31 43 31 39 31 33 39 31 39 3B 76 65 72 73 3D 31 2E 30 3B 74 79 70 65 3D 31 33 35 3B 6E 68 33 3D 31 31 2E 36 37 3B 68 32 73 3D 31 30 2E 38 38 3B 72 73 73 69 3D 31 31 3B 73 6E 72 3D 31 37 3B 63 6F 75 6E 74 3D 34 32 39 31 0A"
# byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
# ascii_string = byte_string.decode("ascii")

# print("555",ascii_string,"666")


# 污水检测modbus解析------------------------------------------------------
# modbus_frame = "01 03 38 3D 6F 97 C1 3E 69 0D 4E 3E 08 52 7C 43 EF A0 FE 00 12 00 34 00 01 4D A7 00 12 00 34 00 01 4D A7 41 45 70 A4 46 40 E6 66 3F 90 20 50 3F E9 E2 04 43 79 19 9A 00 00 00 01 4C 53"
#             #b'\x01\x038\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x9b{\xce\x00\x00\x00\x00\x00\x00\x00\x00\xc4s'
#             #b'\x01\x038\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x9a\xa1\xd9\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf6'

# tail = modbus_frame.find("4C 53")
# input_list = modbus_frame[9:tail-1]
# output_list = []
# for i in range(0, len(input_list), 12):
#     cur = input_list[i:i+11]
#     print("i:",i)
#     print(cur,"xx")
#     if i <= 36 or (i >= 96 and i <= 144):
#         # byte_sequence = "3E 69 0D 4E"
#         # 将字节序列转换为字节串
#         print(cur)
#         byte_string = bytes.fromhex(cur)
#         print(byte_string)
#         # 解析为浮点数
#         float_value = struct.unpack('>f', byte_string)[0]
#         # 输出结果
#         print("解析的浮点数:", float_value)
    # if (i >= 48 and i <= 84) or i == 156:
    #     byte_string = bytes.fromhex(cur)
    #     print(byte_string)
    #     # 解析为整数
    #     integer_value = int.from_bytes(byte_string, byteorder='big')
    #     # 输出结果
    #     print("解析的整数:", integer_value)
# 污水检测modbus解析------------------------------------------------------

# 污水检测兆腾传过来的数据，转化成上面01 03 38的形式的字符串-----------------
# import binascii

# data = b'\x01\x038\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x9a\xa1\xd9\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf6'

# # 使用binascii.hexlify()将字节序列转换为目标形式
# hex_representation = binascii.hexlify(data).decode()

# print(hex_representation)

# 污水检测兆腾传过来的数据，转化成上面01 03 38的形式的字符串-----------------

# data = b'\xff\r\t\x01shlk2210002'

# # 使用切片操作提取 "shlk2210002"
# result = data[4:].decode()

# print(result)

byte_sequence = "3E690D4E"
# 3E 69 0D 4E 液位，高前低后。3E 69 0D 4E=0.2275898米
byte_string = bytes.fromhex(byte_sequence)
print(byte_string)
# 解析为浮点数
float_value = struct.unpack('>f', byte_string)[0]
# 输出结果
print("解析的浮点数:", float_value)