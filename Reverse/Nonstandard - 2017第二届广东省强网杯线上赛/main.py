s = "nAdtxA66nbbdxA71tUAE2AOlnnbtrAp1nQzGtAQGtrjC7==="
table = "zYxWvUtSrQpOnMlKjIhGfEdCbA765321"

def find(x):
    if(x=='='):
        return 0
    return table.index(x)

result = ''

for i in range(len(s)//8):
    p = s[i*8:i*8+8]
    t = 0
    for j in p:
        t = t<<5
        t += find(j)
    for j in range(5):
        result = result + chr((t&0xff00000000)>>32)
        t = t<<8

print result


# flag{f1ag_1s_enc0de_bA3e32!}

# zYxWvUtSrQpOnMlKjIhGfEdCbA765321

# nAdtxA66nbbdxA71tUAE2AOlnnbtrAp1nQzGtAQGtrjC7===

print p
print t