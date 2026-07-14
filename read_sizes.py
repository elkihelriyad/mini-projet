import os
import struct

p = r'c:\Users\Riyad_Uks\Desktop\images'
for f in os.listdir(p):
    if f.endswith('.png'):
        try:
            with open(os.path.join(p, f), 'rb') as fp:
                data = fp.read(24)
                if data[:8] == b'\x89PNG\r\n\x1a\n':
                    w, h = struct.unpack('>II', data[16:24])
                    print(f"{f}: {w}x{h}")
        except Exception as e:
            print(f"Error {f}: {e}")
