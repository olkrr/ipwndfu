import subprocess
import sys
import typing

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def apply_patches(
    binary: bytes, patches: typing.Sequence[typing.Tuple[int, bytes]]
) -> bytes:
    for (offset, data) in patches:
        binary = binary[:offset] + data + binary[offset + len(data) :]
    return binary


def aes_decrypt(data: bytes, iv: bytes, key: bytes) -> bytes:
    cipher = Cipher(algorithm=algorithms.AES(key), mode=modes.CBC(iv))
    decrypter = cipher.decryptor()

    return decrypter.update(data) + decrypter.finalize()


def hex_dump(data: bytes, address: int) -> bytes:
    p = subprocess.Popen(
        ["xxd", "-o", str(address)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (stdout, stderr) = p.communicate(input=data)

    if p.returncode != 0 or len(stderr) > 0:
        print(f"ERROR: xxd failed: {stderr!r}")
        sys.exit(1)

    return stdout
