"""繁體 (default) / 简体 for messages made on the Python side (errors etc.).

Messages are written in Simplified Chinese (the first argument of tr); the
Traditional version is made from it with Taiwan wording (hant.py). The second
argument (English) is not used in this edition.

The page sends its language ('hant' or 'hans') with every request; the server
sets it for the thread that handles the request and passes it on to downloads.
"""
import threading

from .hant import to_hant

_local = threading.local()


def set_lang(lang):
    _local.lang = 'hans' if lang == 'hans' else 'hant'


def get_lang():
    return getattr(_local, 'lang', 'hant')


def tr(hans, en=''):  # noqa: ARG001 - English is not shown in this edition
    return hans if get_lang() == 'hans' else to_hant(hans)
