string = b'h`ahawFD``djpvl Tmiim'
username = ""
password = ""
for i in range(12):
    username = username + chr( i ^ int( ord(string[i]) ) )

for i in range(9):
    password = password + chr( i ^ int( ord(string[i + 12]) ) )

print username
print password