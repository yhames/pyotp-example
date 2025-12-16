import base64


def encode_base32(input_string: str) -> str:
    """문자열을 Base32로 인코딩합니다."""
    # 문자열을 bytes로 변환
    byte_data = input_string.encode("utf-8")
    # Base32 인코딩
    base32_bytes = base64.b32encode(byte_data)
    # 다시 문자열로 변환
    return base32_bytes.decode("utf-8")


def main():
    text = input("Base32로 변환할 문자열 입력: ")
    encoded = encode_base32(text)
    print(encoded)


if __name__ == "__main__":
    main()
