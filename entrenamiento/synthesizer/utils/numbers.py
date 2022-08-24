import re
import inflect

_inflect = inflect.engine()
_comma_number_re = re.compile(r"([0-9][0-9\,]+[0-9])")
_decimal_number_re = re.compile(r"([0-9]+\.[0-9]+)")
_pounds_re = re.compile(r"£([0-9\,]*[0-9]+)")
_dollars_re = re.compile(r"\$([0-9\.\,]*[0-9]+)")
_ordinal_re = re.compile(r"[0-9]+(ero|ndo|to|ésimo)")
_number_re = re.compile(r"[0-9]+")


def _remove_commas(m):
  return m.group(1).replace(",", "")


def _expand_decimal_point(m):
  return m.group(1).replace(".", " punto ")


def _expand_dollars(m):
  match = m.group(1)
  parts = match.split(".")
  if len(parts) > 2:
    return match + " dólares"  # Unexpected format
  dollars = int(parts[0]) if parts[0] else 0
  cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if dollars and cents:
    dollar_unit = "dólar" if dollars == 1 else "dólares"
    cent_unit = "céntimo" if cents == 1 else "céntimos"
    return "%s %s, %s %s" % (dollars, dollar_unit, cents, cent_unit)
  elif dollars:
    dollar_unit = "dólar" if dollars == 1 else "dólares"
    return "%s %s" % (dollars, dollar_unit)
  elif cents:
    cent_unit = "céntimo" if cents == 1 else "céntimos"
    return "%s %s" % (cents, cent_unit)
  else:
    return "cero dólares"


def _expand_ordinal(m):
  return _inflect.number_to_words(m.group(0))


def _expand_number(m):
  num = int(m.group(0))
  if num > 1000 and num < 3000:
    if num == 2000:
      return "dos mil"
    elif num > 2000 and num < 2010:
      return "dos mil " + _inflect.number_to_words(num % 100)
    elif num % 100 == 0:
      return _inflect.number_to_words(num // 100) + " ciento"
    else:
      return _inflect.number_to_words(num, andword="", zero="cero", group=2).replace(", ", " ")
  else:
    return _inflect.number_to_words(num, andword="")


def normalize_numbers(text):
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_pounds_re, r"\1 libras", text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point, text)
  text = re.sub(_ordinal_re, _expand_ordinal, text)
  text = re.sub(_number_re, _expand_number, text)
  return text
