# program for conveting the log.txt file to easily readable file

"""
Warning: -- This program does not works all the time!
"""

input_file = open('log.txt', 'r')
input_string = ''
for char in input_file:
    input_string += char

input_string = input_string.split(' ')

# loop through the string arrary
output_string = ''
for data in input_string:
    if data == 'Return':
        output_string += '<Return>\n'
    elif data == 'space':
        output_string += ' '
    elif data == 'BackSpace':
        output_string = output_string[:-1]
    elif data == 'minus':
        output_string += '-'
    elif data == 'equal':
        output_string += '='
    elif data == 'apostrophe':
        output_string == '\''
    elif data == 'question':
        output_string += '?'
    elif data == 'comma':
        output_string += ','
    elif data == 'exclam':
        output_string += '!'
    elif data == 'period':
        output_string += '.'
    elif data == 'colon':
        output_string += ':'
    elif data == 'at':
        output_string += '@'
    elif data == 'semicolon':
        output_string += ';'
    elif data == 'P_End':
        output_string += '<1>'
    elif data == 'P_Down':
        output_string += '<2>'
    elif data == 'P_Next':
        output_string += '<3>'
    elif data == 'P_Left':
        output_string += '<4>'
    elif data == 'P_Begin':
        output_string += '<5>'
    elif data == 'P_Right':
        output_string += '<6>'
    elif data == 'P_Home':
        output_string += '<7>'
    elif data == 'P_Up':
        output_string += '<8>'
    elif data == 'P_Page_Up':
        output_string += '<9>'
    elif data == 'P_Insert':
        output_string += '<0>'
    else:
        if len(data) == 0:
            output_string += ''
        elif len(data) == 1:
            output_string += data
        else:
            output_string += '<' + data + '>'

# finally save the output_string to a input_file
output_file = open('readable_log.txt','w')
output_file.write(output_string)
output_file.close()
input_file.close()
print '-- converted --'
print 'WARNING: This program may produce unexpected results sometimes. Try decoding yourself in such cases!'











#
