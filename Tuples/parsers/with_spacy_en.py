"""
set of functions for producing, easy to work with structure and property parse representations,
via spaCy for english text
"""

import pathlib
import typing
from collections import defaultdict
from itertools import cycle
from pprint import pprint as pp

import orjson
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_lg")

def parse_df(df: pd.DataFrame) -> list[tuple[dict, dict]]:
    return parse_list(nlp.pipe(list(df["text"]), n_process=1))

def parse_list(docs) -> list[tuple[dict, dict]]:
    """Return a list of (structure::dict, properties::dict) tuples, one tuple for each text in texts."""
    return [parse(doc) for doc in docs]

def parse(doc) -> tuple[dict, dict]:
    """Return a (structure::dict, properties::dict) tuple corresponding to the passed nlp(text) output."""
    structured_parse = get_structured(parse_as_list(doc))
    return structured_parse

def parse_as_list(doc) -> list[dict]:
    """Return text as list of token property dicts.
    Note: crucially, each token dict contains an index and index to its immediate head
    enabling the building of a structure.
    """

    output = []
    for i, token in enumerate(doc):

        # NOTE: all real token indices start from 1
        # NOTE: the depindex (i.e., index of head) attributed to root token is 0
        d = {
            "index": token.i + 1,
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "dep": token.dep_,
            "depindex": 0 if token.head.i == token.i else token.head.i + 1,
        }

        output.append(d)

    return output


def get_modifier_to_head(parse: list) -> dict:
    """Return a dict of modifier index<int> : head index<int>, wrt., sentence parse

    Args:
        parse (list[dict]): i.e., the parse
    """
    # build a hash of modifier index<int> : head index<int>, wrt., parse
    modifier_to_head = {int(token["index"]): int(token["depindex"]) for token in parse}

    return modifier_to_head


def get_structured(parse: list) -> tuple:
    """Return (structure::dict, properties::dict) tuple corresponding to the parse"""

    structure = defaultdict(list)
    modifier_to_head = get_modifier_to_head(parse)

    # populate stucture
    for m_index, h_index in modifier_to_head.items():
        structure[h_index].append(m_index)

    # populate
    properties = {token["index"]: token for token in parse}

    return (dict(structure), properties)
