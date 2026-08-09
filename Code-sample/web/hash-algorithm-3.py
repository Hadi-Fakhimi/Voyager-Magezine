#our simple hash function
def digit_hash(input_text):
    sum = 0
    for ch in input_text:
        #multiply by a larger prime number (like 31 or 131) to increase the impact of the character position
        sum = (sum * 31) + ord(ch)    #ord -> give ASCII binary number of the character

    result = sum % 100000000    #the remainder is divided by 100,000,000, to get 8 digits
    return result

#call our hash function with different words
print(digit_hash("AB"))
print(digit_hash("B#"))