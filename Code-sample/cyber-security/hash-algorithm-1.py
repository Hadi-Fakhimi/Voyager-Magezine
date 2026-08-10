#how hash work?
import hashlib    #python hashing library

#our inputs
text1 = 'hello'
text2 = 'Hello'

#converting 8-bit unicode(python 3 defult) to bytecode of 8-bit unicode
encodeText1 = text1.encode('utf-8')
encodeText2 = text2.encode('utf-8')

#parse a text expression into characters and convert each to a binary number
print('show the raw data (binary form) of text 1 & 2 (for each character):')
for ch in text1:
    print(ch, ':', ord(ch), sep='', end='\t')    #ord -> give ASCII binary number of the character

print(end='\n')

for ch in text2:
    print(ch, ':', ord(ch), sep='', end='\t')    #ord -> give ASCII binary number of the character

print(end='\n\n')

#parse a text expression into characters and convert each to a hexadecimal number
print('show the raw data of text 1 & 2 (in hexadecimal form for each character):')
for ch in text1:
    print(ch, ':', hex(ord(ch)), sep='', end='\t')    #hex(ord) -> give ASCII hex number of the character

print(end='\n')

for ch in text2:
    print(ch, ':', hex(ord(ch)), sep='', end='\t')    #hex(ord) -> give ASCII hex number of the character

print(end='\n\n')

#converting to hash (MD5 is 128-bit)
hash_code1 = hashlib.md5(encodeText1).hexdigest()
hash_code2 = hashlib.md5(encodeText2).hexdigest()

#print our output
print("the first word in MD5 hash: ", hash_code1)
print("the second word in MD5 hash:", hash_code2)