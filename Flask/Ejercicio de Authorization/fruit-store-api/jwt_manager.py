from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt


BASE_DIR = Path(__file__).resolve().parent


class JWTManager:
    def __init__(self, private_key_path: str, public_key_path: str):
        with open(private_key_path, "r") as file:
            self.private_key = file.read()

        with open(public_key_path, "r") as file:
            self.public_key = file.read()

    def encode(self, data: dict) -> str:
        payload = data.copy()

        payload["exp"] = (
            datetime.now(timezone.utc)
            + timedelta(hours=2)
        )

        return jwt.encode(
            payload,
            self.private_key,
            algorithm="RS256",
        )

    def decode(self, token: str):
        return jwt.decode(
            token,
            self.public_key,
            algorithms=["RS256"],
        )


jwt_manager = JWTManager(
    private_key_path=str(BASE_DIR / "private_key.pem"),
    public_key_path=str(BASE_DIR / "public_key.pem"),
)