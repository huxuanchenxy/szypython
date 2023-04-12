import struct
import binascii

bytes = b'\x43\xEF\xA0\xFE'
float_value = struct.unpack('>f', bytes)[0]

print(float_value)



hex_string = "68 65 61 72 74 3D 6F 6B 0A"
byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
ascii_string = byte_string.decode("ascii")

print("11",ascii_string,"22")






hex_string = "69 6D 65 69 3D 33 35 35 39 35 32 30 39 36 35 30 32 31 36 39 3B 63 63 69 64 3D 38 39 38 36 30 34 41 33 31 39 32 31 43 31 39 31 33 38 38 32 3B 76 65 72 73 3D 31 2E 30 3B 74 79 70 65 3D 31 33 35 3B 6E 68 33 3D 31 31 2E 37 33 3B 68 32 73 3D 38 2E 31 36 3B 72 73 73 69 3D 31 35 3B 73 6E 72 3D 31 33 3B 63 6F 75 6E 74 3D 31 33 0A"
byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
ascii_string = byte_string.decode("ascii")

print("11",ascii_string,"22")


hex_string = "63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A"
byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
ascii_string = byte_string.decode("ascii")

print("11",ascii_string,"22")

hex_string = "63 6F 6E 6E 65 63 74 3D 6F 6B 0A"
byte_string = binascii.unhexlify(hex_string.replace(" ", ""))
ascii_string = byte_string.decode("ascii")

print("11",ascii_string,"22")
