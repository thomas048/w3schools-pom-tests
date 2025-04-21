class LoginData:
    INVALID_EMAIL_FORMATS = [
        ("12345678", "12345678", "Please enter a valid email address"),
        ("test@", "12345678", "Please enter a valid email address"),
        ("test@test", "12345678", "Please enter a valid email address"),
        ("test.com", "12345678", "Please enter a valid email address"),
        ("@test.com", "12345678", "Please enter a valid email address")
    ]

    VALID_CREDENTIALS = {
        "email": "chan.pktest63@gmail.com",
        "password": "A1234567890_a"
    }

    EMPTY_CREDENTIALS = {
        "email": "",
        "password": "",
        "error": "Please enter your email and password"
    }
