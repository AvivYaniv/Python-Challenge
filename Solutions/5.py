import pickle

pkl_file = open('banner.p', 'rb')

banner = pickle.load(pkl_file)

complete = ""
for b in banner:
    complete += '\n'
    for c in b:
        complete += c[0] * int(c[1])

print complete
        
pkl_file.close()
