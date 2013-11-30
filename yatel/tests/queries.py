#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# CONSTANTS
#===============================================================================

VALID = []
INVALID = []


#===============================================================================
# QUERIES
#===============================================================================

VALID.append(
    {'function': {'name': 'describe'}, 'id': 1, 'type': 'Descriptor'}
)

VALID.append({
    "id": 251255,
    "function": {
        "name": "variable",
        "args": [
            {'type': 'dict', 'value': {'hola': {'type': 'literal', 'value': 1}}}
        ]
    }
})

VALID.append({
    "id": 1545454845,
    "function": {
        "name": "haplotype_by_id",
        "args": [
            {
                "type": "literal",
                "function": {
                    "name": "slice",
                    "kwargs": {
                        "iterable": {"type": "unicode", "value": "id_01_"},
                        "f": {"type": "int", "value": "-3"},
                        "t": {"type": "int", "value": "-1"}
                    }
                }
            }
        ]
    }
})