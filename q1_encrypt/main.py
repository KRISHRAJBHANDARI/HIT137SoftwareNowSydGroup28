"""
HIT137 Assignment 2 — Question 1
Encrypt, decrypt, and verify per spec.

Rules (summarised):
- Lowercase:
  a–m: shift forward by (shift1 * shift2)
  n–z: shift backward by (shift1 + shift2)
- Uppercase:
  A–M: shift backward by (shift1)
  N–Z: shift forward by (shift2 ** 2)
- Non-letters unchanged.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict

# ---- Paths ----
ROOT = Path(__file__).resolve().parent         
PROJECT = ROOT.parent                            
DATA_DIR = PROJECT / "data"
OUT_DIR = PROJECT / "outputs"

RAW_FILE_1 = DATA_DIR / "raw_text.txt"          
RAW_FILE_2 = ROOT / "raw_text.txt"               
RAW_FILE_3 = PROJECT / "raw_text.txt"            

ENC_FILE = OUT_DIR / "encrypted_text.txt"
DEC_FILE = OUT_DIR / "decrypted_text.txt"


def _wrap_shift(ch: str, k: int) -> str:
    """Shift a single alphabetic char by k positions (can be negative), preserving case."""
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + k) % 26))
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + k) % 26))
    return ch


def _build_encryption_map(shift1: int, shift2: int) -> Dict[str, str]:
    """Build mapping for every letter to its encrypted counterpart (exact rules)."""
    m: Dict[str, str] = {}
    k_lower_first = shift1 * shift2        # a–m -> forward
    k_lower_second = -(shift1 + shift2)    # n–z -> backward
    k_upper_first = -shift1                # A–M -> backward
    k_upper_second = (shift2 ** 2)         # N–Z -> forward

    for c in map(chr, range(ord("a"), ord("z") + 1)):
        m[c] = _wrap_shift(c, k_lower_first if "a" <= c <= "m" else k_lower_second)
    for c in map(chr, range(ord("A"), ord("Z") + 1)):
        m[c] = _wrap_shift(c, k_upper_first if "A" <= c <= "M" else k_upper_second)
    return m


def _invert_mapping(m: Dict[str, str]) -> Dict[str, str]:
    return {v: k for k, v in m.items()}


def encrypt_text(text: str, enc_map: Dict[str, str]) -> str:
    return "".join(enc_map.get(ch, ch) for ch in text)


def decrypt_text(text: str, dec_map: Dict[str, str]) -> str:
    return "".join(dec_map.get(ch, ch) for ch in text)


def read_raw_text() -> tuple[str, Path]:
    """Find and read raw_text.txt from known locations; return (text, path_used)."""
    for candidate in (RAW_FILE_1, RAW_FILE_2, RAW_FILE_3):
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8")
            return text, candidate
    raise FileNotFoundError(
        "raw_text.txt not found.\n"
        f"Looked in:\n  {RAW_FILE_1}\n  {RAW_FILE_2}\n  {RAW_FILE_3}\n"
        "Place raw_text.txt in one of those locations."
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def verify_files(a: Path, b: Path) -> bool:
    return a.read_text(encoding="utf-8") == b.read_text(encoding="utf-8")


def main() -> None:
    print("============= HIT137 A2 - Q1: Encrypt/Decrypt/Verify =============")
    while True:
        try:
            shift1 = int(input("Enter shift1 (integer): ").strip())
            shift2 = int(input("Enter shift2 (integer): ").strip())
            break
        except ValueError:
            print("Please enter valid integers for shift1 and shift2.")

    enc_map = _build_encryption_map(shift1, shift2)
    dec_map = _invert_mapping(enc_map)

    # Read input
    raw_text, src_path = read_raw_text()
    print(f"[INFO] Read {len(raw_text)} chars from: {src_path}")

    if len(raw_text) == 0:
        print("[WARN] Input file has 0 characters. Outputs will also be empty. "
              "Please put content in raw_text.txt and run again.")

    # Encrypt → write
    encrypted = encrypt_text(raw_text, enc_map)
    write_text(ENC_FILE, encrypted)
    print(f"[INFO] Wrote {len(encrypted)} chars to: {ENC_FILE}")

    # Decrypt → write
    decrypted = decrypt_text(encrypted, dec_map)
    write_text(DEC_FILE, decrypted)
    print(f"[INFO] Wrote {len(decrypted)} chars to: {DEC_FILE}")

    ok = verify_files(src_path, DEC_FILE)
    print(f"Verification: {'Success :)' if ok else 'Failed!'}")


if __name__ == "__main__":
    main()
