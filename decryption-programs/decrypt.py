import sys

passKey = 0
message = ''

def getPassKey(password):
	key = 1
	count = 0
	for char in password:
		if count%2 == 0:
			key *= ord(char)
		else:
			key += ord(char)
		count += 1
	return key

def decrypt(word):
    if len(word) == 0:
        return ''
    word = int(word)
    word = (word//passKey) - passKey
    return chr(word)

if len(sys.argv) == 1:
    print '-- enter password to decrypt --'
else:
    passKey = getPassKey(sys.argv[1])
    file = open('sys.conf', 'r')
    data = ''
    for c in file:
        data += c
    data = data.split(' ')
    i = 0
    while i < len(data):
        if data[i] == '/':
            temp_message = ''
            i += 1
            while data[i] != '/':
                temp_message += decrypt(data[i])
                i += 1
            message += temp_message + ' '
        else:
            message += decrypt(data[i]) + ' '
        i += 1
    output_file = open('log.txt', 'w')
    output_file.write(message)
    print '-- decrypted --'
