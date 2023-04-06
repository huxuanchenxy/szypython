import struct

bytes = b'\x43\xEF\xA0\xFE'
float_value = struct.unpack('>f', bytes)[0]

print(float_value)