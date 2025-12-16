import os
import pyotp
import qrcode
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# TOTP 객체 생성
totp = pyotp.TOTP(os.getenv("TOTP_SECRET"))

# 프로비저닝 URI 생성
uri = totp.provisioning_uri(name="admin@example.com", issuer_name="MyAdmin")

# QR 코드 이미지 생성
img = qrcode.make(uri)

# 파일로 저장
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "totp_qr.png")
img.save(file_path)

print("✅ QR 코드가 'totp_qr.png' 파일로 저장되었습니다.")