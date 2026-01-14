#Input for shift amount 1 and 2
shift_1=int(input("enter shift 1:"))
shift_2=int(input("enter shift 2:"))
def encryption(shift1,shift2):
        """  Encrypts the contents of 'raw_text.txt' and writes the result to 'encrypted_text.txt'.

    The function reads the text from 'raw_text.txt' and applies a custom two-shift
    encryption. Uppercase and lowercase letters are treated differetly :
    - Uppercase letters 'A'-'M' are shifted backwards by shift1 modulo 13.
    - Uppercase letters 'N'-'Z' are shifted forwards by the square of shift2 modulo 13.
    - Lowercase letters 'a'-'m' are shifted forwards by (shift1 * shift2) modulo 13.
    - Lowercase letters 'n'-'z' are shifted forwards by (shift1 + shift2) modulo 13.
    
    Note on modulo 13:
    The function uses modulo 13 instead of modulo 26 because the encryption applies 
    different rules to the first and second halves of the alphabet (A-M / N-Z and a-m / n-z). 
    Modulo 13 ensures that each letter stays within its half during encryption and decryption.
    Using modulo 26 would cause letters to potentially cross halves, making decryption 
    inconsistent.
    Non-alphabetic characters are left unchanged.
        Args:
            shift1 (_int_): 1st shift num
            shift2 (_int_): 2nd shift num
        Returns:
        None: The encrypted text is saved to 'encrypted_text.txt'.
        """
        with open('raw_text.txt', 'r') as f:
            Text = f.read()
        
        result=""
        for char in Text:
            if char.isupper():
                pos=ord(char)-ord('A')#convert into number rank
                if pos<13:#for (a-m)#Seperation in the one and second half in 26 alphabet letters
                    shifted=(pos-shift1)%13
                else:#for (m-z)
                    pos_relative=pos-13
                    shifted_relative=(pos_relative+(shift2**2))%13
                    shifted=shifted_relative+13
                result+=chr(shifted+ord('A'))
            elif char.islower():
                pos=ord(char)-ord('a')
                if pos<13:
                    shifted=(pos+(shift1*shift2))%13
                else:
                    pos_relative=pos-13
                    shifted_relative=(pos_relative+(shift1+shift2))%13
                    shifted=shifted_relative+13
                result+=chr(shifted+ord('a'))
            else:
                result+=char
        with open("encrypted_text.txt","w") as f:
            f.write(result)
            
def decryption(shift1,shift2):
        """Decrypts the contents of 'encrypted_text.txt' and writes the original text 
        to 'decrypted_text.txt'.

        The function reads the text from 'encrypted_text.txt' and reverses the custom 
        two-shift encryption applied by the `encryption` function. Uppercase and 
        lowercase letters are treated differently:
        - Uppercase letters 'A'-'M' are shifted forwards by shift1 modulo 13.
        - Uppercase letters 'N'-'Z' are shifted backwards by the square of shift2 modulo 13.
        - Lowercase letters 'a'-'m' are shifted backwards by (shift1 * shift2) modulo 13.
        - Lowercase letters 'n'-'z' are shifted backwards by (shift1 + shift2) modulo 13.
        Non-alphabetic characters are left unchanged.

        Args:
            shift1 (_int_): The first shift value used during encryption.
            shift2 (_int_): The second shift value used during encryption.

        Returns:
        None: The decrypted text is saved to 'decrypted_text.txt'.
        """
        with open("encrypted_text.txt","r") as f:
            Text=f.read()
        result=""
        for char in Text:
            if char.isupper():
                pos=ord(char)-ord('A')
                if pos<13:
                    shifted=(pos+shift1)%13
                else:
                    pos_relative=pos-13
                    shifted_relative=(pos_relative-(shift2**2))%13
                    shifted=shifted_relative+13
                result+=chr(shifted+ord('A'))
            elif char.islower():
                pos=ord(char)-ord('a')
                if pos<13:
                    shifted=(pos-(shift1*shift2))%13
                else:
                    pos_relative=pos-13
                    shifted_relative=(pos_relative-(shift1+shift2))%13
                    shifted=shifted_relative+13
                result+=chr(shifted+ord('a'))
            else:
                result+=char
        with open("decrypted_text.txt","w") as f:
            f.write(result)
def verification(orignal,decrypted):
    """This function simply compares orginal and decrypted message string and prints
    messages

    Args:
        orignal (_string_): the orginal text message.
        decrypted (_string_):the decrypted message obtained from decryption function.
    """
    
    if orignal==decrypted:
        print("encryption and decryption sucessful")
    else:
        print("decryption failed")
        
encrypted_file=encryption(shift_1,shift_2)    
decrypted_file= decryption(shift_1,shift_2)
with open('raw_text.txt', 'r') as f:
            Orginal_msg = f.read()
with open("decrypted_text.txt","r") as f:
            decrypted_msg=f.read()
verification(Orginal_msg,decrypted_msg)

      

