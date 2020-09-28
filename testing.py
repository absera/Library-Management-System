class Message:
    def __init__(self, message, key, pq):
        self.message = str(message).upper()  # original message
        self.key = key  # the keys (a, b)
        self.pq = pq  # two even numbers that give self.key[1]
        self.cipher = ""  # encrypted message
        self.decrypted_message = ""  # decrypted message
        self.reference_alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # alphabet in the message
        self.reference_alphabet_list = [char for char in self.reference_alphabet]  # alphabet but as a list

    def Encrypt(self):
        """
        Takes self.message and iterate through it and get each character's index in the alphabet.
        applies the RSA algorithm equations to each character.
        stores it as one string in self.cipher
        """
        for i in self.message:
            digit_number = self.reference_alphabet_list.index(i)
            final_reference_number = digit_number ** self.key[0]
            mod_number = final_reference_number % self.key[1]

            self.cipher += self.reference_alphabet[mod_number]
        return self.cipher

    def GenerateDecryptionKey(self):
        """
        Generates decryption key according to RSA algorithm.
        returns the smallest co-prime number with self.key[0] and fN
        """
        # N = self.pq[0] * self.pq[1]
        fN = (self.pq[0] - 1) * (self.pq[1] - 1)
        d = None
        i = 1
        while i < 100:
            if (self.key[0] * i) % fN == 1:
                d = i
                break
            i += 1
        return d

    def Decrypt(self):
        """
        Takes the cipher text self.cipher and applies RSA decryption algorithm to it.
        returns it as new string called self.decrypted_message
        """
        decryption_key = self.GenerateDecryptionKey()
        for i in self.cipher:
            digit_number = self.reference_alphabet_list.index(i)
            final_reference_number = digit_number ** decryption_key
            mod_number = final_reference_number % self.key[1]

            self.decrypted_message += self.reference_alphabet[mod_number]
        return self.decrypted_message


message1 = Message(" Abcdefghijklmn", (5, 14), (2, 7))
print(message1.Encrypt())
print(message1.Decrypt())
