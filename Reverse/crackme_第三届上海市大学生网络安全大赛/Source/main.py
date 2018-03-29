flag = 'dcsdscdbwbadsdabwaacwcacadsdwbdcdbwc'
table = 'dssdwasawawaaswddw'
my_flag = ''
j =0 
for i in range(len(table) / 2):
    my_flag = my_flag + table[j]
    my_flag = my_flag + ' '
    my_flag = my_flag + table[j + 1]
    my_flag = my_flag + ' '
    j = j + 2
print flag
print my_flag