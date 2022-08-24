"""
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You"ll typically want to use:
  1. "spanish_cleaners" for Spanish text
  2. "transliteration_cleaners" for non-Spanish text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
"""

import re
from unidecode import unidecode
from .numbers import normalize_numbers

# Regular expression matching whitespace:
_whitespace_re = re.compile(r"\s+")

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1]) for x in [
  ("lic", "licenciado"),
  ("mag", "magister"),
  ("dr", "doctor"),
  ("co", "colombia"),
  ("jr", "jirón"),
  ("av", "avenida"),
  ("gen", "generación"),
  ("sgt", "siguiente"),
  ("q", "que"),
  ("x", "por"),
  ("pq", "porque"),
  ("ps", "pues"),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text):
  return normalize_numbers(text)


def lowercase(text):
  """lowercase input tokens."""
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, " ", text)


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  """Basic pipeline that lowercases and collapses whitespace without transliteration."""
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  """Pipeline for non-Spanish text that transliterates to ASCII."""
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def spanish_cleaners(text):
  """Pipeline for Spanish text, including number and abbreviation expansion."""
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  return text
