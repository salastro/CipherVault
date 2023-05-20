# This is a program to encrypt/decrypt a message using several ciphers.
import random
import string
import enchant
MORSE_CODE_DICT= {'A': '.-', 'B': '-...',  'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                'I': '..', 'J': '.---', 'K': '-.-','L': '.-..', 'M': '--', 'N': '-.','O': '---', 'P': '.--.', 'Q': '--.-',
                'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--','X': '-..-', 'Y': '-.--', 'Z': '--..',
                '1': '.----', '2': '..---', '3': '...--','4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
                '0': '-----', ', ': '--..--', '.': '.-.-.-','?': '..--..', '/': '-..-.', '-': '-....-','(': '-.--.', ')': '-.--.-','$/': ' '}


def run_program(FirstTime):
    if FirstTime :
        print("Hi, this is CipherVault! \nI can help you encrypt/decrypt any message you want.")
        print("First, use how do you want to enter your message?")

    message = enter_text()
    while True:
        programType = input("Encrypt or Decrypt?(E or D): ")
        if programType == 'E' or programType == 'D':
            break
        else:
            print("Invalid input, please try again.")
    while True:
        cipherType = input("Enter which cipher you want to code into:(C,V,R,M) ")
        if cipherType == 'C' or cipherType == 'V' or cipherType == 'R' or cipherType == 'M':
            break
        else:
            print("Invalid input, please try again.")
    if cipherType == 'C':
        result = caeser_cipher(message,programType)
        print("Your possible shifts are: ", result)
        if input("Save it to a file?(Y or N): ") == 'Y':
            save_message_to_file(result,'Caeser Cipher.txt')
        FirstTime = False
        run_program(FirstTime)
        
    elif cipherType == 'V':
        if programType == 'E':
            while True:
                if input("Use a random key?(Y or N): ") == 'Y':
                    key = generate_random_key(4,8)
                    print("Your key is: ",key)
                    break
                elif input("Use a random key?(Y or N): ") == 'N':
                    key = input("Enter the keyword: ")
                    break
                else:
                    print("Error!, try again.")
                
            result = vigenere_encrypt(message, key)
            print("Your message is: ", result)
            if input("Save it to a file?(Y or N): ") == 'Y':
                save_message_to_file(result,'Vigenere Cipher.txt')
        else:
            while True:
                key = input("Enter the keyword: ")
                if key == '':
                    print("Empty can't be a key, Please try again.")
                else:
                    break
            result = vigenere_decrypt(message, key)
            print('Your message is: ', result)
            if input("Save it to a file?(Y or N): ") == 'Y':
                save_message_to_file(result,'Vigenere Cipher.txt')
        FirstTime = False
        run_program(FirstTime)
    elif cipherType == 'R':
        while True:
            try:
                key = int(input("Please enter the number of lines (Only integer): "))
                break
            except ValueError:
                print("That is not an integer. Please try again.")
        if programType == 'E':
            result = Railfencecipher(message, key)
            print('Your message is: ', result)
            if input("Save it to a file?(Y or N): ") == 'Y':
                save_message_to_file(result,'Rail-Fence Cipher.txt')
        else:
            result = Rail_fence_decipher(message, key)
            print('Your message is: ', result)
            if input("Save it to a file?(Y or N): ") == 'Y':
                save_message_to_file(result,'Rail-Fence Cipher.txt')
        FirstTime = False
        run_program(FirstTime)
    elif cipherType == 'M':
        if programType == 'E':
            result = morse_code_cipher(message)
            print('Your message is: ', result)
            if input("Save it to a file?(Y or N): ") == 'Y':
                save_message_to_file(result,'Morse code.txt')
        else:
            result = Morse_code_decipher(message)
            print('Your message is: ', result)
            if input("Save it to a file?(Y or N): ") == 'Y':
                save_message_to_file(result,'Morse code.txt')
        FirstTime = False
        run_program(FirstTime)


def generate_random_key(min_length, max_length):
    length = random.randint(min_length, max_length)
    word = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return word


def enter_text():
    # Make sure the input is always 1 or 2
    while True:
        method = input("Enter '1' for typing directly through the program, Enter '2' for loading it from a file: ")
        if method != '1' and method != '2':
            print("Invalid Input!")
        else:
            break
    if method == '1':     # Type input directly into the program
        message = input("Enter the message: ")
    elif method == '2':
        message = read_message_from_file()

    if message == '':
        print("Your message is empty, Please try again.")
        enter_text()
    else:
        return message


def read_message_from_file():
    location = input("Enter the location of the txt file: ")
    with open(location,  'r') as file:
        message = file.read()    
    return message


def caeser_cipher(message, programType):
    if programType == 'E':
        while True:
            try:
                shiftVal = int(input("Please enter the shift value (Only integer): "))
                break
            except ValueError:
                print("That is not an integer. Please try again.")
    else:
        while True:
            key = input("Got the key? (Y or N)")
            if key == 'Y':
                while True:
                    try:
                        shiftVal = int(input("Please enter the shift value (Only integer): "))
                        break
                    except ValueError:
                        print("That is not an integer. Please try again.")
                break
            elif key == 'N':
                return automatic_caeser_decipher(message)
            else:
                print("Wrong input. Please try again.")
                
        shiftVal = shiftVal * -1
    return shift_text(message,shiftVal)


def automatic_caeser_decipher(message):
    
    d = enchant.Dict("en_US")
    bestScore = 0
    bestShift = 0
    multipleScore = []
    multipleShifts = []
    for shift in range(1,26):
        score = 0
        shiftedMessage = shift_text(message,shift).split()
        for word in shiftedMessage:
            if d.check(word):
                score +=1
        
        if score > bestScore:
            bestScore = score
            bestShift = shift
            multipleScore.append([shift, score])
        elif score == bestScore and bestScore != 0:
            multipleScore.append([shift, score])
    if len(multipleScore) > 0:
        for scoreList in multipleScore:
            if scoreList[1] >= bestScore:
                multipleShifts.append(shift_text(message, scoreList[0]))
        return multipleShifts
    else:
        return shift_text(message, bestShift),26 - bestShift

    


def vigenere_encrypt(plaintext, keyword):
    ciphertext = ""
    keyword = keyword.upper()
    i = 0
    for c in plaintext:
        if c.isalpha():
            # Shift the letter forward by the corresponding letter in the keyword
            shift = ord(keyword[i % len(keyword)]) - ord('A')
            if c.isupper():
                ciphertext += chr((ord(c) + shift - 65) % 26 + 65)
            else:
                ciphertext += chr((ord(c) + shift - 97) % 26 + 97)
            i += 1
        else:
            ciphertext += c
    return ciphertext


def vigenere_decrypt(ciphertext, keyword):
    plaintext = ""
    keyword = keyword.upper()
    i = 0
    for c in ciphertext:
        if c.isalpha():
            # Shift the letter backwards by the corresponding letter in the keyword
            shift = ord(keyword[i % len(keyword)]) - ord('A')
            if c.isupper():
                plaintext += chr((ord(c) - shift - 65) % 26 + 65)
            else:
                plaintext += chr((ord(c) - shift - 97) % 26 + 97)
            i += 1
        else:
            plaintext += c
    return plaintext


def shift_text(message, shiftVal):
    shiftedMessage = ''
    for i in range(len(message)):
        if message[i].isupper():
            shiftedMessage += chr((ord(message[i]) - 65 + shiftVal)%26 + 65)
        elif message[i].islower():
            shiftedMessage += chr((ord(message[i]) - 97 + shiftVal)%26 + 97)
        else:
            shiftedMessage += message[i]
    return shiftedMessage


def Railfencecipher(cleartext, key):
    result = ""

    matrix = [["" for x in range(len(cleartext))] for y in range(key)]

    increment = 1
    row = 0
    col = 0

    for c in cleartext:
        matrix[row][col] = c
        if row == 0:
            increment = 1
        elif row == key - 1:
            increment = -1

        row += increment
        col += 1

    for list in matrix:
        result += "".join(list)
    return result


def transpose(matrix):
    
    result = [[0 for y in range(len(matrix))] for x in range(len(matrix[0]))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result[j][i] = matrix[i][j]
    
    return result


def Rail_fence_decipher(cipheredtext, key):
    
    result = ""

    matrix = [["" for x in range(len(cipheredtext))] for y in range(key)]

    index = 0
    increment = 1

    for SelectedRow in range(len(matrix)):
        row = 0

        for col in range(len(matrix[ row ])):
            if row + increment < 0 or row + increment >= len(matrix):
                increment = increment * -1
            
            if row == SelectedRow: 
                matrix[row][col] += cipheredtext[index]
                index += 1
            
            row += increment
    
    matrix = transpose(matrix)

    for list in matrix:
        result+= "".join(list)
    return result


def morse_code_cipher(cleartext):
    MORSE_CODE_DICT= {'A': '.-', 'B': '-...',  'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                'I': '..', 'J': '.---', 'K': '-.-','L': '.-..', 'M': '--', 'N': '-.','O': '---', 'P': '.--.', 'Q': '--.-',
                'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--','X': '-..-', 'Y': '-.--', 'Z': '--..',
                '1': '.----', '2': '..---', '3': '...--','4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
                '0': '-----', ', ': '--..--', '.': '.-.-.-','?': '..--..', '/': '-..-.', '-': '-....-','(': '-.--.', ')': '-.--.-'}


    message= cleartext.upper()
    encrypted_message=[]

    for c in message:
        if c == ' ':
            encrypted_message.append(' $/ ')
        else:
            encrypted_message.append(MORSE_CODE_DICT[c]+' ')

    encrypted_message= "".join(encrypted_message)

    return encrypted_message


def Morse_code_decipher(ciphered_message):
    MORSE_CODE_DICT_INV= {v: k for k, v in MORSE_CODE_DICT.items()}

    encrypted_message= ciphered_message

    morse_words= encrypted_message.split()

    decrypted_message= ""
    for morse_word in morse_words:
        decrypted_message += MORSE_CODE_DICT_INV.get(morse_word, " ")

    return decrypted_message


def save_message_to_file(message, fileName):
    with open(fileName, 'w') as file:
        file.write(message)


FirstTime = True
run_program(FirstTime)
