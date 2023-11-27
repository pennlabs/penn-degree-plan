from functools import reduce
from operator import and_, or_

from django.db.models import Q
from lark import Lark, Transformer


"""
This file contains a parser for that can convert a stringified Q object
(ie, repr(Q(...))) back into a Q object. Note that this parser
relies on the stability of the Q object __repr__ method. Run the associated
tests to make sure the output of Q(...).__repr__ is as expected and that this
parser re-builds the Q object correctly.

Note that when you manually test this parser against strings, you'll want to use
raw strings (ie, q_object_parser.parse(r"..."))
"""


class QObjectTransformer(Transformer):
    """
    This class transforms the Abstract Syntax Tree (AST) generated by the parser
    into a usable Python object.
    """

    def list(self, n):
        """
        List of values should just be a Python list.
        """
        return list(n)

    def and_clause(self, clauses):
        return reduce(and_, clauses, Q())

    def or_clause(self, clauses):
        return reduce(or_, clauses, Q())

    def not_clause(self, clauses):
        (clause,) = clauses
        return ~clause

    def condition(self, n):
        key, value = n
        return Q(**{key: value})

    def string(self, s):
        (s,) = s
        return bytes(s[1:-1], "utf-8").decode("unicode_escape")  # strip off quotes

    def sint(self, n):
        (n,) = n
        return int(n)

    def sfloat(self, n):
        (n,) = n
        return float(n)

    def none(self, n):
        return None

    def q(self, n):
        (clause,) = n
        return clause


q_object_parser = Lark(
    r"""
    q: "<Q:" clause ">"

    ?clause: condition
           | and_clause
           | or_clause
           | not_clause
          // NOTE: XOR clauses are not supported (yet...)

    ?connector_clause: and_clause
                    | or_clause

    condition: "(" string "," value ")"
    and_clause:"(AND:" [clause ("," clause)*] ")"
    or_clause: "(OR:" [clause ("," clause)*] ")"
    not_clause: "(NOT" connector_clause ")"

    ?value: string
          | SIGNED_INT -> sint
          | SIGNED_FLOAT -> sfloat
          | none

    none: "None"
    string: /'.*?(?<!\\)(\\\\)*?'/ // escapable strings
          | /".*?(?<!\\)(\\\\)*?"/

    %import common.SIGNED_INT
    %import common.SIGNED_FLOAT
    %import common.WS
    %import common._STRING_ESC_INNER
    %ignore WS
    """,
    start="q",
    transformer=QObjectTransformer(),
    parser="lalr",
)
