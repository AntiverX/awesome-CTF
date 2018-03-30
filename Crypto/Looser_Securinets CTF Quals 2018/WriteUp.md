# Reference

http://cherryblog.in/securinetsctf-quals-2018-write-up-hacking-competition/

# Title

Can you help me recover the picture ?

# Content

At first i thought it is a png image so renamed again and again but nothing was work able.
We know header of PNG file, so we can XOR the existing header with what we expect, and therefore extract the potential XOR key.So lets find key.

```Python
from crypto_commons.generic import xor, xor_string
def main():
    with open('flag.png.crypt', 'rb') as f:
        data = f.read()
        png_header = [137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 0xd, 0x49, 0x48, 0x44, 0x52, 0x0, 0x0]
        result = xor(png_header, map(ord, data[:len(png_header)]))
        key = "".join([chr(c) for c in result]) + ("\0" * (18 - len(png_header)))
        print(key.encode("hex"))
        with open('result.png', 'wb') as f:
            f.write(xor_string(data, key * (len(data) / len(key))))

main()
```

whole file is encrypted with single byte key ‘e’. So i got original image after decryption.

Flag: Flag{Hopefully_headers_are_constants}