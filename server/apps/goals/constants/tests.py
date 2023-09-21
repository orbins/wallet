from typing import Final


class DefaultTestData:
    USER_DATA: Final[dict[str, str]] = {
        "email": "test@test.com",
        "username": "user",
        "password": "password"
    }
    INITIAL_BALANCE = 100000
