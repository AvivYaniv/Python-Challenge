import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php")
print str(proxy.phone('Bert'))

# 555-ITALY
# print str(proxy.phone('Bert'))

# He is not the evil
# print str(proxy.phone('bert'))

# {'introspection': {'specUrl': 'http://phpxmlrpc.sourceforge.net/doc-2/ch10.html', 'specVersion': 2}, 'system.multicall': {'specUrl': 'http://www.xmlrpc.com/discuss/msgReader$1208', 'specVersion': 1}, 'xmlrpc': {'specUrl': 'http://www.xmlrpc.com/spec', 'specVersion': 1}}
# print str(proxy.system.getCapabilities())

# Returns the phone of a person
# print str(proxy.system.methodHelp('phone'))

# [['string', 'string']]
# print str(proxy.system.methodSignature('phone'))

# ['phone', 'system.listMethods', 'system.methodHelp', 'system.methodSignature', 'system.multicall', 'system.getCapabilities']
# print str(proxy.system.listMethods())
