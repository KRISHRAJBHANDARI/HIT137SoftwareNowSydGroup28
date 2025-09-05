# HIT137 Assignment 2 — Question 1
# Encrypt, decrypt, and verify per spec.
#
# Group Name: SYDN 28
# Group Members:
#  - Krish Rajbhandari - S395754
#  - Noor-E-Sefat Ahmed - S394047
#  - Mehedi Hasan - S395003
#  - Suyog Kadariya - S393829
#
# What this program does:
# 1) Ask the user for two numbers (shift1 and shift2).
# 2) Read the text from raw_text.txt by checking common locations.
# 3) Encrypt the text using the rules given in the question.
# 4) Decrypt it back using the reverse mapping.
# 5) Check that the decrypted text matches the original and print Success/Failed mesaage.
#
# Encryption rules we were given:
# - Lowercase:
#     a–m = move forward by (shift1 * shift2)
#     n–z = move backward by (shift1 + shift2)
# - Uppercase:
#     A–M = move backward by (shift1)
#     N–Z = move forward by (shift2 ** 2)
# - Everything else (spaces, punctuation, numbers) stays the same.

from __future__ import annotations
from pathlib import Path
from typing import Dict

# Declaring File/folder locations
# We try these paths so the marker can run from different folders without errors.
ROOT = Path(__file__).resolve().parent        # this script's folder
PROJECT = ROOT.parent                         # project root (one level up)
DATA_DIR = PROJECT / "data"
OUT_DIR = PROJECT / "outputs"

# We look for raw_text.txt in these places
RAW_FILE_1 = DATA_DIR / "raw_text.txt"        
RAW_FILE_2 = ROOT / "raw_text.txt"           
RAW_FILE_3 = PROJECT / "raw_text.txt"       

# Output files will be written here
ENC_FILE = OUT_DIR / "encrypted_text.txt"
DEC_FILE = OUT_DIR / "decrypted_text.txt"


def _wrap_shift(ch: str, k: int) -> str:
    """
    Move a letter by k places (can be negative). We keep case the same and wrap
    around the alphabet using % 26. If it's not a letter, we just return it.
    """
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + k) % 26))
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + k) % 26))
    return ch  # non-letters unchanged


def _build_encryption_map(shift1: int, shift2: int) -> Dict[str, str]:
    """
    Make a dictionary that tells us how each letter changes when we encrypt.
    Example: {'a': 'k', 'b': 'l', ...}. We do this separately for lower/upper
    and for the two halves of the alphabet as the rules say.
    """
    m: Dict[str, str] = {}

    # Work out the actual step sizes from the two numbers the user typed.
    k_lower_first = shift1 * shift2        # a–m: forward by this
    k_lower_second = -(shift1 + shift2)    # n–z: backward by this
    k_upper_first = -shift1                # A–M: backward by this
    k_upper_second = (shift2 ** 2)         # N–Z: forward by this

    # Fill the map for lowercase letters
    for c in map(chr, range(ord("a"), ord("z") + 1)):
        if "a" <= c <= "m":
            m[c] = _wrap_shift(c, k_lower_first)
        else:
            m[c] = _wrap_shift(c, k_lower_second)

    # Fill the map for uppercase letters
    for c in map(chr, range(ord("A"), ord("Z") + 1)):
        if "A" <= c <= "M":
            m[c] = _wrap_shift(c, k_upper_first)
        else:
            m[c] = _wrap_shift(c, k_upper_second)

    return m


def _invert_mapping(m: Dict[str, str]) -> Dict[str, str]:
    """
    Turn the encryption dictionary around so we can decrypt.
    If 'a' → 'k' when encrypting, then 'k' → 'a' when decrypting.
    """
    return {v: k for k, v in m.items()}


def encrypt_text(text: str, enc_map: Dict[str, str]) -> str:
    """Go through the text character by character and replace using enc_map."""
    return "".join(enc_map.get(ch, ch) for ch in text)


def decrypt_text(text: str, dec_map: Dict[str, str]) -> str:
    """Do the reverse replacement using the decryption map."""
    return "".join(dec_map.get(ch, ch) for ch in text)


def read_raw_text() -> tuple[str, Path]:
    """
    Try to read raw_text.txt from a few possible places.
    We return the text and the path we actually used so we can verify later.
    """
    for candidate in (RAW_FILE_1, RAW_FILE_2, RAW_FILE_3):
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8")
            return text, candidate
    # If we get here, none of the locations had the file.
    raise FileNotFoundError(
        "raw_text.txt not found.\n"
        f"Looked in:\n  {RAW_FILE_1}\n  {RAW_FILE_2}\n  {RAW_FILE_3}\n"
        "Place raw_text.txt in one of those locations."
    )


def write_text(path: Path, text: str) -> None:
    """Create the folder if needed and save the text to the file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def verify_files(a: Path, b: Path) -> bool:
    """Simple check: the decrypted text should be exactly the same as the original."""
    return a.read_text(encoding="utf-8") == b.read_text(encoding="utf-8")


def main() -> None:
    print("============= HIT137 A2 - Q1: Encrypt/Decrypt/Verify =============")

    # Get the two numbers from the user. We loop until the user types valid ints.
    while True:
        try:
            shift1 = int(input("Enter shift1 (integer): ").strip())
            shift2 = int(input("Enter shift2 (integer): ").strip())
            break
        except ValueError:
            print("Please enter valid integers for shift1 and shift2.")

    # Build the letter, letter encryption map using the rules,
    # then flip it so we can also decrypt.
    enc_map = _build_encryption_map(shift1, shift2)
    dec_map = _invert_mapping(enc_map)

    # Read the original text
    raw_text, src_path = read_raw_text()
    print(f"[INFO] Read {len(raw_text)} chars from: {src_path}")

    if len(raw_text) == 0:
        # Not an error, but a friendly heads-up. The program still runs.
        print("[WARN] Input file has 0 characters. Outputs will also be empty. "
              "Please put content in raw_text.txt and run again.")

    # Encrypt the original text and save it
    encrypted = encrypt_text(raw_text, enc_map)
    write_text(ENC_FILE, encrypted)
    print(f"[INFO] Wrote {len(encrypted)} chars to: {ENC_FILE}")

    # Decrypt the encrypted text and save it
    decrypted = decrypt_text(encrypted, dec_map)
    write_text(DEC_FILE, decrypted)
    print(f"[INFO] Wrote {len(decrypted)} chars to: {DEC_FILE}")

       # Final check: did we get back exactly what we started with?
    ok = verify_files(src_path, DEC_FILE)
    print(f"Verification: {'Success :)' if ok else 'Failed!'}")


# Program starts here
if __name__ == "__main__":
    main()