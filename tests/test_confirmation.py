from app.agent.confirmation import (
    detect_confirmation,
    extract_aadhaar,
    extract_otp,
    extract_pan,
)


class TestConfirmation:
    def test_hindi_yes(self):
        assert detect_confirmation("haan") is True
        assert detect_confirmation("Haan ji") is True
        assert detect_confirmation("theek hai") is True
        assert detect_confirmation("kar do") is True

    def test_english_yes(self):
        assert detect_confirmation("yes") is True
        assert detect_confirmation("Yes please") is True
        assert detect_confirmation("ok") is True
        assert detect_confirmation("confirm") is True

    def test_hindi_no(self):
        assert detect_confirmation("nahi") is False
        assert detect_confirmation("mat karo") is False
        assert detect_confirmation("nah") is False

    def test_english_no(self):
        assert detect_confirmation("no") is False
        assert detect_confirmation("cancel") is False
        assert detect_confirmation("reject") is False

    def test_unclear(self):
        assert detect_confirmation("mujhe sochna hai") is None
        assert detect_confirmation("tell me more") is None

    def test_deny_overrides_confirm(self):
        assert detect_confirmation("nahi, mat karo") is False


class TestExtraction:
    def test_extract_aadhaar(self):
        assert extract_aadhaar("mera aadhaar 1234 5678 9012 hai") == "123456789012"
        assert extract_aadhaar("123456789012") == "123456789012"
        assert extract_aadhaar("no number here") is None

    def test_extract_otp(self):
        assert extract_otp("OTP hai 456789") == "456789"
        assert extract_otp("123456") == "123456"
        assert extract_otp("12345") is None

    def test_extract_pan(self):
        assert extract_pan("PAN ABCDE1234F") == "ABCDE1234F"
        assert extract_pan("abcde1234f") == "ABCDE1234F"
        assert extract_pan("no pan") is None
