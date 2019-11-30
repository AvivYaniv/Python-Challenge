import md5

mybroken = open("mybroken.zip", "rb").read()
for position in range(len(mybroken)):
    pre_error = mybroken[:position]
    post_error = mybroken[position+1:]
    for fix_char in range(256):
        myrepaired = pre_error + chr(fix_char) + post_error
        if md5.md5(myrepaired).hexdigest() == 'bbb8b499a0eef99b52c7f13f4e78c24b':
            open("myrepaired.zip","wb").write(myrepaired)

print "Done repairing Zip Levl: 24"
