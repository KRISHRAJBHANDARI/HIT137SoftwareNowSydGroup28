# HIT137 Assignment 2 - Question 1 (final, mask-based)
# Student: Mahedy Hasan, ID: S395003

def classify_char(c):
    """Return mask code for the original character's group."""
    if c.islower():
        return 'l' if 'a' <= c <= 'm' else 'L'
    if c.isupper():
        return 'u' if 'A' <= c <= 'M' else 'U'
    return '-'

def encrypt_char(c, s1, s2):
    """Encrypt one char according to the rules."""
    if not c.isalpha():
        return c
    if c.islower():
        idx = ord(c) - ord('a')
        if idx <= 12:  # a-m
            idx = (idx + s1 * s2) % 26
        else:          # n-z
            idx = (idx - (s1 + s2)) % 26
        return chr(idx + ord('a'))
    else:
        idx = ord(c) - ord('A')
        if idx <= 12:  # A-M
            idx = (idx - s1) % 26
        else:          # N-Z
            idx = (idx + (s2 ** 2)) % 26
        return chr(idx + ord('A'))

def decrypt_char(c, mask, s1, s2):
    """Decrypt one char using the original-group mask."""
    if mask == '-':
        return c  # non-letters unchanged

    if mask == 'l':   # original was lowercase a-m -> encryption added + s1*s2
        if c.islower():
            idx = (ord(c) - ord('a') - (s1 * s2)) % 26
            return chr(idx + ord('a'))
    elif mask == 'L': # original was lowercase n-z -> encryption did - (s1 + s2)
        if c.islower():
            idx = (ord(c) - ord('a') + (s1 + s2)) % 26
            return chr(idx + ord('a'))
    elif mask == 'u': # original was uppercase A-M -> encryption did - s1
        if c.isupper():
            idx = (ord(c) - ord('A') + s1) % 26
            return chr(idx + ord('A'))
    elif mask == 'U': # original was uppercase N-Z -> encryption did + s2^2
        if c.isupper():
            idx = (ord(c) - ord('A') - (s2 ** 2)) % 26
            return chr(idx + ord('A'))

    # Fallback: if types somehow disagree, just return as-is (shouldn't happen)
    return c

def encrypt_file(s1, s2):
    with open("raw_text.txt", "r", encoding="utf-8", newline="") as f:
        raw = f.read()

    encrypted = []
    mask = []

    for ch in raw:
        mask_code = classify_char(ch)
        mask.append(mask_code)
        encrypted.append(encrypt_char(ch, s1, s2))

    with open("encrypted_text.txt", "w", encoding="utf-8", newline="") as f:
        f.write("".join(encrypted))

    with open("enc_mask.txt", "w", encoding="utf-8", newline="") as f:
        f.write("".join(mask))

    print("Encrypted file created: encrypted_text.txt")
    print("Mask file created: enc_mask.txt")

def decrypt_file(s1, s2):
    with open("encrypted_text.txt", "r", encoding="utf-8", newline="") as f:
        enc = f.read()
    with open("enc_mask.txt", "r", encoding="utf-8", newline="") as f:
        mask = f.read()

    # Ensure lengths align
    if len(enc) != len(mask):
        print("Warning: mask length mismatch; decryption may fail.")
    n = min(len(enc), len(mask))

    dec_chars = [decrypt_char(enc[i], mask[i], s1, s2) for i in range(n)]
    # Append any trailing chars (unlikely) without change
    if len(enc) > n:
        dec_chars.append(enc[n:])

    with open("decrypted_text.txt", "w", encoding="utf-8", newline="") as f:
        f.write("".join(dec_chars))

    print("Decrypted file created: decrypted_text.txt")

def verify():
    with open("raw_text.txt", "r", encoding="utf-8", newline="") as a, \
         open("decrypted_text.txt", "r", encoding="utf-8", newline="") as b:
        same = a.read() == b.read()
    print("Verification SUCCESS!" if same else "Verification FAILED!")
    return same

if __name__ == "__main__":
    print("=== Question 1: Encryption & Decryption ===")
    s1 = int(input("Enter shift1: "))
    s2 = int(input("Enter shift2: "))

    encrypt_file(s1, s2)
    decrypt_file(s1, s2)
    verify()
