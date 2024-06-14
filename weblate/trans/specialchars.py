# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Helper code to get user special characters specific for given language."""

import unicodedata

from django.conf import settings
from django.utils.translation import gettext, gettext_lazy

# Names of hardcoded characters
CHAR_NAMES = {
    "\t": gettext_lazy("Insert tab character"),
    "\n": gettext_lazy("Insert new line"),
    "…": gettext_lazy("Insert horizontal ellipsis"),
    "\u00ad": gettext_lazy("Insert a soft hyphen"),
    "\u00a0": gettext_lazy("Insert a non-breaking space"),
}
DISPLAY_CHARS = {"\t": "↹", "\n": "↵", "\u00ad": "﹙-﹚"}


HYPHEN_LANGS = {
    "af",
    "am",
    "ar",
    "ast",
    "az",
    "bg",
    "bs",
    "ca",
    "cs",
    "cy",
    "da",
    "de",
    "dsb",
    "dz",
    "ee",
    "el",
    "en",
    "eo",
    "es",
    "fa",
    "fi",
    "fr",
    "fy",
    "gd",
    "gl",
    "gu",
    "he",
    "hr",
    "hsb",
    "id",
    "is",
    "ja",
    "ka",
    "kk",
    "kn",
    "ko",
    "ksh",
    "ky",
    "lb",
    "lkt",
    "lt",
    "lv",
    "mk",
    "mn",
    "mr",
    "nl",
    "os",
    "pa",
    "pl",
    "pt",
    "ro",
    "ru",
    "sk",
    "sr",
    "sv",
    "ta",
    "th",
    "to",
    "tr",
    "uz",
    "vi",
    "vo",
    "yi",
    "zh",
}

EN_DASH_LANGS = {
    "af",
    "am",
    "ar",
    "ast",
    "az",
    "bg",
    "bs",
    "ca",
    "cs",
    "cy",
    "da",
    "de",
    "dsb",
    "dz",
    "ee",
    "el",
    "en",
    "eo",
    "es",
    "fi",
    "fr",
    "fy",
    "gd",
    "gl",
    "gu",
    "he",
    "hr",
    "hsb",
    "hu",
    "id",
    "is",
    "ka",
    "kk",
    "kn",
    "ksh",
    "ky",
    "lb",
    "lkt",
    "lt",
    "lv",
    "mk",
    "mn",
    "mr",
    "nb",
    "nl",
    "os",
    "pa",
    "pl",
    "pt",
    "ro",
    "ru",
    "sk",
    "sr",
    "sv",
    "ta",
    "th",
    "to",
    "tr",
    "uk",
    "uz",
    "vi",
    "vo",
    "yi",
    "zh",
}

EM_DASH_LANGS = {
    "af",
    "ar",
    "ast",
    "az",
    "bg",
    "bs",
    "ca",
    "cy",
    "de",
    "dsb",
    "dz",
    "ee",
    "el",
    "en",
    "eo",
    "es",
    "fr",
    "fy",
    "gd",
    "gl",
    "gu",
    "he",
    "hr",
    "hsb",
    "id",
    "is",
    "it",
    "ja",
    "ka",
    "kk",
    "kn",
    "ko",
    "ksh",
    "ky",
    "lb",
    "lkt",
    "lt",
    "lv",
    "mk",
    "mn",
    "mr",
    "nl",
    "os",
    "pa",
    "pl",
    "pt",
    "ro",
    "ru",
    "sv",
    "ta",
    "th",
    "to",
    "tr",
    "uz",
    "vi",
    "vo",
    "yi",
    "zh",
}

EXTRA_CHARS = {
    "brx": ("।", "॥"),
    "he": ("־", "״", "׳"),
}

# Additional characters for RTL languages
RTL_CHARS = (8204, 8205, 8206, 8207, 8234, 8235, 8236, 8237, 8238)


def get_quote(code, data, name):
    """Return special char for quote."""
    if code in data:
        return name, data[code], data[code]
    return name, data["ALL"], data["ALL"]


def get_display_char(char):
    name = short = char
    if unicodedata.category(char)[0] in {"C", "Z"}:
        # Various control and space characters
        try:
            name = unicodedata.name(char)
            short = "".join(
                x[0] for x in name.replace("-TO-", " ").replace("-", " ").split()
            )
        except ValueError:
            # Char now known to unicode data
            # This mostly happens for control characters < 0x20
            name = short = char.encode("unicode_escape").decode("ascii")
    # Use display short name if available
    short = DISPLAY_CHARS.get(char, short)
    return name, short


def format_char(char):
    """Return verbose description of a character."""
    name, short = get_display_char(char)
    if char in CHAR_NAMES:
        return CHAR_NAMES[char], short, char

    return gettext("Insert character {0}").format(name), short, char


def get_special_chars(language, additional="", source=""):
    """Return list of special characters."""
    for char in settings.SPECIAL_CHARS:
        yield format_char(char)
    code = language.code.replace("_", "-").split("-")[0]

    if code in EXTRA_CHARS:
        for char in EXTRA_CHARS[code]:
            yield format_char(char)

    yield get_quote(code, MAIN_OPEN, gettext("Main opening quote"))
    yield get_quote(code, MAIN_CLOSE, gettext("Main closing quote"))
    yield get_quote(code, ALT_OPEN, gettext("Alternative opening quote"))
    yield get_quote(code, ALT_CLOSE, gettext("Alternative closing quote"))

    if code in HYPHEN_LANGS:
        yield format_char("\u00ad")
        yield gettext("Hyphen"), "‐", "‐"

    if code in EN_DASH_LANGS:
        yield gettext("En dash"), "–", "–"

    if code in EM_DASH_LANGS:
        yield gettext("Em dash"), "—", "—"

    for char in additional:
        name, short = get_display_char(char)
        yield gettext("User configured character: {}").format(name), short, char

    rtl = language.direction == "rtl"
    for char in set(source):
        try:
            name = unicodedata.name(char)
        except ValueError:
            continue
        if "ARROW" in name:
            if rtl and "LEFT" in name:
                try:
                    char = unicodedata.lookup(name.replace("LEFT", "RIGHT"))
                except KeyError:
                    continue
                yield format_char(char)
            elif rtl and "RIGHT" in name:
                try:
                    char = unicodedata.lookup(name.replace("RIGHT", "LEFT"))
                except KeyError:
                    continue
                yield format_char(char)
            else:
                yield format_char(char)


RTL_CHARS_DATA = [format_char(chr(c)) for c in RTL_CHARS]

# Quotes data, generated using scripts/generate-specialchars
ALT_OPEN = {
    "ALL": "‘",
    "af": "‘",
    "agq": "‚",
    "ak": "‘",
    "am": "‹",
    "ar": "‘",
    "as": "‘",
    "asa": "‘",
    "ast": "“",
    "az": "‹",
    "bas": "„",
    "be": "‹",
    "bem": "‘",
    "bez": "‘",
    "bg": "‚",
    "bm": "“",
    "bn": "‘",
    "bo": "‘",
    "br": "‹",
    "brx": "‘",
    "bs": "‘",
    "ca": "“",
    "cgg": "‘",
    "chr": "‘",
    "cs": "‚",
    "cy": "‘",
    "da": "›",
    "de": "‚",
    "dsb": "‚",
    "dua": "‘",
    "dyo": "“",
    "ee": "‘",
    "el": "“",
    "en": "‘",
    "eo": "‘",
    "es": "“",
    "et": "‚",
    "eu": "‹",
    "ewo": "“",
    "fa": "‹",
    "ff": "‚",
    "fi": "’",
    "fil": "‘",
    "fo": "‘",
    "fr": "‹",
    "fur": "“",
    "ga": "‘",
    "gl": "‘",
    "gsw": "‹",
    "gu": "‘",
    "gv": "‘",
    "ha": "‘",
    "haw": "‘",
    "he": "‚",
    "hi": "‘",
    "hr": "‚",
    "hsb": "‚",
    "hu": "»",
    "hy": "‘",
    "ia": "“",
    "id": "‘",
    "ig": "‘",
    "ii": "‘",
    "is": "‚",
    "it": "“",
    "ja": "『",
    "jgo": "‹",
    "jmc": "‘",
    "ka": "‚",
    "kab": "“",
    "kam": "‘",
    "kde": "‘",
    "kea": "‘",
    "ki": "‘",
    "kk": "‘",
    "kkj": "‹",
    "kl": "‘",
    "km": "‘",
    "kn": "‘",
    "ko": "‘",
    "kok": "‘",
    "ksb": "‘",
    "ksh": "‚",
    "kw": "‘",
    "ky": "„",
    "lag": "’",
    "lb": "‚",
    "lg": "‘",
    "ln": "‘",
    "lt": "‚",
    "lu": "‘",
    "luo": "‘",
    "luy": "‚",
    "lv": "„",
    "mas": "‘",
    "mfe": "‘",
    "mg": "“",
    "mk": "‚",
    "ml": "‘",
    "mr": "‘",
    "ms": "‘",
    "mt": "‘",
    "mua": "“",
    "my": "‘",
    "naq": "‘",
    "nb_NO": "‘",
    "nd": "‘",
    "ne": "‘",
    "nl": "‘",
    "nmg": "«",
    "nn": "‘",
    "nnh": "“",
    "nr": "“",
    "nso": "“",
    "nyn": "‘",
    "om": "‘",
    "or": "‘",
    "os": "„",
    "pa": "‘",
    "pl": "«",
    "ps": "‘",
    "pt": "‘",
    "rm": "‹",
    "rn": "’",
    "ro": "«",
    "rof": "‘",
    "ru": "„",
    "rw": "‘",
    "rwk": "‘",
    "saq": "‘",
    "se": "’",
    "seh": "‘",
    "ses": "‘",
    "sg": "“",
    "shi": "„",
    "si": "‘",
    "sk": "‚",
    "sl": "‚",
    "sn": "’",
    "so": "‘",
    "sq": "‚",
    "sr": "‚",
    "sr_Cyrl": "‘",
    "sr_Latn": "‚",
    "ss": "“",
    "sv": "’",
    "sw": "‘",
    "ta": "‘",
    "te": "‘",
    "teo": "‘",
    "th": "‘",
    "ti": "‘",
    "tn": "“",
    "to": "‘",
    "tr": "‘",
    "ts": "“",
    "tzm": "‘",
    "ug": "›",
    "uk": "„",
    "ur": "‘",
    "uz": "‘",
    "uz_Latn": "‘",
    "vai": "‘",
    "ve": "“",
    "vi": "‘",
    "vo": "‘",
    "vun": "‘",
    "wae": "‹",
    "xog": "‘",
    "yav": "«",
    "yi": "'",
    "yo": "‘",
    "zgh": "„",
    "zh": "『",
    "zh_Hans": "‘",
    "zh_Hant": "『",
    "zu": "‘",
}
ALT_CLOSE = {
    "ALL": "’",
    "af": "’",
    "ak": "’",
    "am": "›",
    "ar": "’",
    "as": "’",
    "asa": "’",
    "ast": "”",
    "az": "›",
    "bas": "“",
    "be": "›",
    "bem": "’",
    "bez": "’",
    "bg": "‘",
    "bm": "”",
    "bn": "’",
    "bo": "’",
    "br": "›",
    "brx": "’",
    "bs": "’",
    "ca": "”",
    "cgg": "’",
    "chr": "’",
    "cs": "‘",
    "cy": "’",
    "da": "‹",
    "de": "‘",
    "dsb": "‘",
    "dua": "’",
    "dyo": "”",
    "ee": "’",
    "el": "”",
    "en": "’",
    "eo": "’",
    "es": "”",
    "et": "‘",
    "eu": "›",
    "ewo": "”",
    "fa": "›",
    "ff": "’",
    "fi": "’",
    "fil": "’",
    "fo": "’",
    "fr": "›",
    "fur": "”",
    "ga": "’",
    "gl": "’",
    "gsw": "›",
    "gu": "’",
    "gv": "’",
    "ha": "’",
    "haw": "’",
    "he": "’",
    "hi": "’",
    "hr": "‘",
    "hsb": "‘",
    "hu": "«",
    "hy": "’",
    "ia": "”",
    "id": "’",
    "ig": "’",
    "ii": "’",
    "is": "‘",
    "it": "”",
    "ja": "』",
    "jgo": "›",
    "jmc": "’",
    "ka": "‘",
    "kab": "”",
    "kam": "’",
    "kde": "’",
    "kea": "’",
    "ki": "’",
    "kk": "’",
    "kkj": "›",
    "kl": "’",
    "km": "’",
    "kn": "’",
    "ko": "’",
    "kok": "’",
    "ksb": "’",
    "ksh": "‘",
    "kw": "’",
    "ky": "“",
    "lag": "’",
    "lb": "‘",
    "lg": "’",
    "ln": "’",
    "lt": "‘",
    "lu": "’",
    "luo": "’",
    "luy": "‘",
    "lv": "“",
    "mas": "’",
    "mfe": "’",
    "mg": "”",
    "mk": "‘",
    "ml": "’",
    "mr": "’",
    "ms": "’",
    "mt": "’",
    "mua": "”",
    "my": "’",
    "naq": "’",
    "nb_NO": "’",
    "nd": "’",
    "ne": "’",
    "nl": "’",
    "nmg": "»",
    "nn": "’",
    "nnh": "”",
    "nr": "”",
    "nso": "”",
    "nyn": "’",
    "om": "’",
    "or": "’",
    "os": "“",
    "pa": "’",
    "pl": "»",
    "ps": "’",
    "pt": "’",
    "rm": "›",
    "rn": "’",
    "ro": "»",
    "rof": "’",
    "ru": "“",
    "rw": "’",
    "rwk": "’",
    "saq": "’",
    "seh": "’",
    "ses": "’",
    "sg": "”",
    "shi": "”",
    "si": "’",
    "sk": "‘",
    "sl": "‘",
    "sn": "’",
    "so": "’",
    "sq": "‘",
    "sr": "‘",
    "sr_Cyrl": "’",
    "sr_Latn": "‘",
    "ss": "”",
    "sv": "’",
    "sw": "’",
    "ta": "’",
    "te": "’",
    "teo": "’",
    "th": "’",
    "ti": "’",
    "tn": "”",
    "to": "’",
    "tr": "’",
    "ts": "”",
    "tzm": "’",
    "ug": "‹",
    "uk": "“",
    "ur": "’",
    "uz": "’",
    "uz_Latn": "’",
    "vai": "’",
    "ve": "”",
    "vi": "’",
    "vo": "’",
    "vun": "’",
    "wae": "›",
    "xog": "’",
    "yav": "»",
    "yi": "'",
    "yo": "’",
    "zgh": "”",
    "zh": "』",
    "zh_Hans": "’",
    "zh_Hant": "』",
    "zu": "’",
}
MAIN_OPEN = {
    "ALL": "“",
    "af": "“",
    "agq": "„",
    "ak": "“",
    "am": "«",
    "ar": "“",
    "as": "“",
    "asa": "“",
    "ast": "«",
    "az": "«",
    "bas": "«",
    "be": "«",
    "bem": "“",
    "bez": "“",
    "bg": "„",
    "bm": "«",
    "bn": "“",
    "bo": "“",
    "br": "«",
    "brx": "“",
    "bs": "“",
    "ca": "«",
    "cgg": "“",
    "chr": "“",
    "cs": "„",
    "cy": "“",
    "da": "»",
    "de": "„",
    "dsb": "„",
    "dua": "«",
    "dyo": "«",
    "ee": "“",
    "el": "«",
    "en": "“",
    "eo": "“",
    "es": "«",
    "et": "„",
    "eu": "«",
    "ewo": "«",
    "fa": "«",
    "ff": "„",
    "fi": "”",
    "fil": "“",
    "fo": "“",
    "fr": "«",
    "fur": "‘",
    "ga": "“",
    "gl": "“",
    "gsw": "«",
    "gu": "“",
    "gv": "“",
    "ha": "“",
    "haw": "“",
    "he": "„",
    "hi": "“",
    "hr": "„",
    "hsb": "„",
    "hu": "„",
    "hy": "“",
    "ia": "‘",
    "id": "“",
    "ig": "“",
    "ii": "“",
    "is": "„",
    "it": "«",
    "ja": "「",
    "jgo": "«",
    "jmc": "“",
    "ka": "„",
    "kab": "«",
    "kam": "“",
    "kde": "“",
    "kea": "“",
    "ki": "“",
    "kk": "“",
    "kkj": "«",
    "kl": "“",
    "km": "“",
    "kn": "“",
    "ko": "“",
    "kok": "“",
    "ksb": "“",
    "ksf": "«",
    "ksh": "„",
    "kw": "“",
    "ky": "«",
    "lag": "”",
    "lb": "„",
    "lg": "“",
    "ln": "“",
    "lt": "„",
    "lu": "“",
    "luo": "“",
    "luy": "„",
    "lv": "«",
    "mas": "“",
    "mfe": "“",
    "mg": "«",
    "mk": "„",
    "ml": "“",
    "mr": "“",
    "ms": "“",
    "mt": "“",
    "mua": "«",
    "my": "“",
    "naq": "“",
    "nb": "«",
    "nb_NO": "«",
    "nd": "“",
    "ne": "“",
    "nl": "“",
    "nmg": "„",
    "nn": "«",
    "nnh": "«",
    "nr": "‘",
    "nso": "‘",
    "nyn": "“",
    "om": "“",
    "or": "“",
    "os": "«",
    "pa": "“",
    "pl": "„",
    "ps": "“",
    "pt": "“",
    "rm": "«",
    "rn": "”",
    "ro": "„",
    "rof": "“",
    "ru": "«",
    "rw": "«",
    "rwk": "“",
    "saq": "“",
    "se": "”",
    "seh": "“",
    "ses": "“",
    "sg": "«",
    "shi": "«",
    "si": "“",
    "sk": "„",
    "sl": "„",
    "sn": "”",
    "so": "“",
    "sq": "„",
    "sr": "„",
    "sr_Cyrl": "“",
    "sr_Latn": "„",
    "ss": "‘",
    "sv": "”",
    "sw": "“",
    "ta": "“",
    "te": "“",
    "teo": "“",
    "th": "“",
    "ti": "“",
    "tn": "‘",
    "to": "“",
    "tr": "“",
    "ts": "‘",
    "tzm": "“",
    "ug": "»",
    "uk": "«",
    "ur": "“",
    "uz": "“",
    "uz_Latn": "“",
    "vai": "“",
    "ve": "‘",
    "vi": "“",
    "vo": "“",
    "vun": "“",
    "wae": "«",
    "xog": "“",
    "yav": "«",
    "yi": '"',
    "yo": "“",
    "zgh": "«",
    "zh": "「",
    "zh_Hans": "“",
    "zh_Hant": "「",
    "zu": "“",
}
MAIN_CLOSE = {
    "ALL": "”",
    "af": "”",
    "ak": "”",
    "am": "»",
    "ar": "”",
    "as": "”",
    "asa": "”",
    "ast": "»",
    "az": "»",
    "bas": "»",
    "be": "»",
    "bem": "”",
    "bez": "”",
    "bg": "“",
    "bm": "»",
    "bn": "”",
    "bo": "”",
    "br": "»",
    "brx": "”",
    "bs": "”",
    "ca": "»",
    "cgg": "”",
    "chr": "”",
    "cs": "“",
    "cy": "”",
    "da": "«",
    "de": "“",
    "dsb": "“",
    "dua": "»",
    "dyo": "»",
    "ee": "”",
    "el": "»",
    "en": "”",
    "eo": "”",
    "es": "»",
    "et": "“",
    "eu": "»",
    "ewo": "»",
    "fa": "»",
    "ff": "”",
    "fi": "”",
    "fil": "”",
    "fo": "”",
    "fr": "»",
    "fur": "’",
    "ga": "”",
    "gl": "”",
    "gsw": "»",
    "gu": "”",
    "gv": "”",
    "ha": "”",
    "haw": "”",
    "he": "”",
    "hi": "”",
    "hr": "“",
    "hsb": "“",
    "hu": "”",
    "hy": "”",
    "ia": "’",
    "id": "”",
    "ig": "”",
    "ii": "”",
    "is": "“",
    "it": "»",
    "ja": "」",
    "jgo": "»",
    "jmc": "”",
    "ka": "“",
    "kab": "»",
    "kam": "”",
    "kde": "”",
    "kea": "”",
    "ki": "”",
    "kk": "”",
    "kkj": "»",
    "kl": "”",
    "km": "”",
    "kn": "”",
    "ko": "”",
    "kok": "”",
    "ksb": "”",
    "ksf": "»",
    "ksh": "“",
    "kw": "”",
    "ky": "»",
    "lag": "”",
    "lb": "“",
    "lg": "”",
    "ln": "”",
    "lt": "“",
    "lu": "”",
    "luo": "”",
    "luy": "“",
    "lv": "»",
    "mas": "”",
    "mfe": "”",
    "mg": "»",
    "mk": "“",
    "ml": "”",
    "mr": "”",
    "ms": "”",
    "mt": "”",
    "mua": "»",
    "my": "”",
    "naq": "”",
    "nb": "»",
    "nb_NO": "»",
    "nd": "”",
    "ne": "”",
    "nl": "”",
    "nn": "»",
    "nnh": "»",
    "nr": "’",
    "nso": "’",
    "nyn": "”",
    "om": "”",
    "or": "”",
    "os": "»",
    "pa": "”",
    "pl": "”",
    "ps": "”",
    "pt": "”",
    "rm": "»",
    "rn": "”",
    "ro": "”",
    "rof": "”",
    "ru": "»",
    "rw": "»",
    "rwk": "”",
    "saq": "”",
    "seh": "”",
    "ses": "”",
    "sg": "»",
    "shi": "»",
    "si": "”",
    "sk": "“",
    "sl": "“",
    "sn": "”",
    "so": "”",
    "sq": "“",
    "sr": "“",
    "sr_Cyrl": "”",
    "sr_Latn": "“",
    "ss": "’",
    "sv": "”",
    "sw": "”",
    "ta": "”",
    "te": "”",
    "teo": "”",
    "th": "”",
    "ti": "”",
    "tn": "’",
    "to": "”",
    "tr": "”",
    "ts": "’",
    "tzm": "”",
    "ug": "«",
    "uk": "»",
    "ur": "”",
    "uz": "”",
    "uz_Latn": "”",
    "vai": "”",
    "ve": "’",
    "vi": "”",
    "vo": "”",
    "vun": "”",
    "wae": "»",
    "xog": "”",
    "yav": "»",
    "yi": '"',
    "yo": "”",
    "zgh": "»",
    "zh": "」",
    "zh_Hans": "”",
    "zh_Hant": "」",
    "zu": "”",
}
