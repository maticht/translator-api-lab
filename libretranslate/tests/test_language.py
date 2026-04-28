from libretranslate.language import fast_guess_language


def test_fast_guess_language_detects_english():
    detected = fast_guess_language("Simple English sentence", ["en", "ru"])

    assert detected is not None
    assert detected["language"] == "en"


def test_fast_guess_language_detects_russian():
    detected = fast_guess_language("Простое русское предложение", ["en", "ru"])

    assert detected is not None
    assert detected["language"] == "ru"


def test_fast_guess_language_returns_none_for_other_language_sets():
    assert fast_guess_language("Hola", ["en", "es"]) is None
