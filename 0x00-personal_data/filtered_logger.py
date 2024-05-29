#!/usr/bin/env python3
""" module for the filter_datum function"""
import re


def filter_datum(fields, redaction, message, separator):
    """ Returns the a log message obfuscated"""

    to_match = f"({'|'.join(fields)})=([^\\{separator}]*)"
    return re.sub(to_match, lambda m: f"{m.group(1)}={redaction}", message)
