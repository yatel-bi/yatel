#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Domain Object Model for Yatel.

"""


#===============================================================================
# ERROR
#===============================================================================

class ValidationError(Exception):
    """Used in function ``dom.validate`` function.

    """
    pass


#===============================================================================
# FACT
#===============================================================================

class Fact(object):
    """The Fact represent a *metadata* of the *haplotype*.

    For example if you relieve in two places the same *haplotype*,
    the characteristics of these places correspond to different *facts* of the
    same *haplotype*.

    """

    def __init__(self, hap_id, **attrs):
        """Creates a new instance

        **Params**
            :hap_id: The ``dom.Haplotype`` id of this fact.
            :attrs: Diferents attributes of this fact.

        """
        self._hap_id = hap_id
        self._attrs = attrs

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return "<{0} for '{1}' at {2}>".format(self.__class__.__name__,
                                                 self._hap_id, hex(id(self)))

    def __eq__(self, obj):
        """x.__eq__(y) <==> x==y"""
        return obj is not None \
            and isinstance(obj, Fact) \
            and hash(self) == hash(obj)

    def __ne__(self, obj):
        """x.__ne__(y) <==> x!=y"""
        return not (self == obj)

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        return hash(str(hash(self._hap_id)) + str(hash(self.items_attrs())))

    def __getattr__(self, n):
        """x.__getattr__('name') <==> x.name <==> x['name']"""
        try:
            return self._attrs[n]
        except KeyError:
            t = type(self).__name__
            msg = "'{t}' object has no attribute '{n}'".format(t=t, n=n)
            raise AttributeError(msg)

    def __getitem__(self, k):
        """x.__getitem__(y) <==> x[y] <==> x.name"""
        return self._attrs[k]

    def items_attrs(self):
        """F.items_attrs() -> an iterator over the (attr_name, attr_value)
        attrs of F.

        """
        return self._attrs.items()

    def names_attrs(self):
        """F.names_attrs() -> an iterator over the attrs names of F.

        """
        return self._attrs.keys()

    def values_attrs(self):
        """F.names_attrs() -> an iterator over the attrs values of F.

        """
        return self._attrs.values()

    def get_attr(self, n, d=None):
        """F.get(n[,d]) -> F[n] if n in F, else d. d defaults to None"""
        return self._attrs.get(n, d)

    @property
    def hap_id(self):
        """The ``dom.Haplotype`` id of this fact."""
        return self._hap_id


#===============================================================================
# HAPLOTYPES
#===============================================================================

class Haplotype(object):
    """Represent a individual class or group with similar characteristics
    to be analized."""

    def __init__(self, hap_id, **attrs):
        """Creates a new instance

        **Params**
            :hap_id: Unique id of this haplotype.
            :attrs: Diferents attributes of this haplotype.

        """
        self._hap_id = hap_id
        self._attrs = attrs

    def __eq__(self, obj):
        """x.__eq__(y) <==> x==y"""
        return obj is not None \
            and isinstance(obj, Haplotype) \
            and hash(self) == hash(obj)

    def __ne__(self, obj):
        """x.__ne__(y) <==> x!=y"""
        return not (self == obj)

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        return hash(self._hap_id)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return "<{0} '{1}' at {2}>".format(self.__class__.__name__,
                                             self._hap_id, hex(id(self)))

    def __getattr__(self, n):
        """x.__getattr__('name') <==> x.name <==> x['name']"""
        try:
            return self._attrs[n]
        except KeyError:
            t = type(self).__name__
            msg = "'{t}' object has no attribute '{n}'".format(t=t, n=n)
            raise AttributeError(msg)

    def __getitem__(self, k):
        """x.__getitem__(y) <==> x[y] <==> x.name"""
        return self._attrs[k]

    def items_attrs(self):
        """H.items_attrs() -> an iterator over the (attr_name, attr_value)
        attrs of F.

        """
        return self._attrs.items()

    def names_attrs(self):
        """H.names_attrs() -> an iterator over the attrs names of F.

        """
        return self._attrs.keys()

    def values_attrs(self):
        """F.names_attrs() -> an iterator over the attrs values of F.

        """
        return self._attrs.values()

    def get_attr(self, n, d=None):
        """H.get(n[,d]) -> H[n] if n in F, else d. d defaults to None"""
        return self._attrs.get(n, d)

    @property
    def hap_id(self):
        """Unique id of this haplotype"""
        return self._hap_id


#===============================================================================
# Edge
#===============================================================================

class Edge(object):
    """Represent a relation between 2 or more *haplotypes*

    """

    def __init__(self, weight, *haps_id):
        """Creates a new instance.

        **Params**
            :weight: The degree of relationship between haplotypes.
            :haps_id: The list of the related haplotypes.

        """
        self._weight = float(weight)
        self._haps_id = haps_id

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return "<{0} '{1} {2}' at {3}>".format(self.__class__.__name__,
                                                 str(self._haps_id),
                                                 self._weight,
                                                 hex(id(self)))

    def __eq__(self, obj):
        """x.__eq__(y) <==> x==y"""
        return obj is not None \
            and isinstance(obj, Edge) \
            and hash(self) == hash(obj)

    def __ne__(self, obj):
        """x.__ne__(y) <==> x!=y"""
        return not (self == obj)

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        return hash(str(hash(self._weight)) + str(hash(tuple(self._haps_id))))

    @property
    def weight(self):
        """The degree of relationship between haplotypes."""
        return self._weight

    @property
    def haps_id(self):
        """The list of the related haplotypes."""
        return self._haps_id


#===============================================================================
# FUNCTIONS
#===============================================================================

def validate(haplotypes, facts, edges):
    """Validate if the *haplotypes*, *facts* and *edges* is part of the same
    network.

    This include:
        - Not duplicated haplotypes id's
        - Existing haplotypes for all facts.
        - Existing haplotypes for all edges

    **Raises**
        Validation error if any of the conditions are not satisfied.

    **Return**
        ``True`` if the network is valid.

    """
    haps_id = set()
    haps_attrs = {}
    for hap in haplotypes:
        if hap.hap_id in haps_id:
            msg = "Duplicated hap_id '{id}'".format(id=hap.hap_id)
            raise ValidationError(msg)
        haps_id.add(hap.hap_id)
        for an, av in [("hap_id", hap.hap_id)] + hap.items_attrs():
            if an not in haps_attrs:
                haps_attrs[an] = type(av)
            elif not isinstance(av, haps_attrs[an]):
                msg = ("Inconsistence of attribute type '{an}' of Haplotype '{hap}'. ",
                       "Types found: '{types}'")
                msg = msg.format(an=an, hap=repr(hap),
                                 types=", ".join([str(facts_attrs[an]),
                                                  str(type(av))]))
                raise ValidationError(msg)

    facts_attrs = {}
    for fact in facts:
        if fact.hap_id not in haps_id:
            msg = "Haplotype id '{id}' of Fact '{fact}' not found on given haplotypes"
            msg = msg.format(id=fact.hap_id, fact=repr(fact))
            raise ValidationError(msg)
        for an, av in [("hap_id", fact.hap_id)] + fact.items_attrs():
            if an not in facts_attrs:
                facts_attrs[an] = type(av)
            elif not isinstance(av, facts_attrs[an]):
                msg = ("Inconsistence of attribute type '{an}' of Fact '{fact}'. "
                       "Types found: '{types}'")
                msg = msg.format(an=an, fact=repr(fact),
                                 types=", ".join([str(facts_attrs[an]),
                                                  str(type(av))]))
                raise ValidationError(msg)

    for edge in edges:
        for hap_id in edge.haps_id:
            if hap_id not in haps_id:
                msg = "Haplotype id '{id}' of edge '{edge}' not found on given haplotypes"
                mag = msg.format(id=edge.hap_id, edge=repr(edge))
                raise ValidationError(msg)
            if not isinstance(edge.weight, (int, float)):
                msg = ("Weight of Edge '{edge}' is not int or float: "
                       "Found '{w}' or type '{t}'")
                msg = msg.format(edge=repr(edge), w=edge.weight,
                                 t=type(edge.weight))
                raise ValidationError(msg)
    return True

#===============================================================================
# cosos para el ale
#===============================================================================

import random

LOCALIDADES = ["RC", "VM", "CBA", "TP", "JC", "PER", "TDV"]
PLANTAS = ["Maiz", "alfalfa", "cebolla", "faso", "tuvieja"]

haps = []
facts = []
edges = []

for idx in xrange(25):
    hap = Haplotype(str(idx),
                    nombre="haplotype_{}".format(idx))
    haps.append(hap)

for hap in haps:
    for idx in xrange(10):
        fact = Fact(hap.hap_id,
                    localidad=random.choice(LOCALIDADES),
                    year=random.randint(1992, 2010),
                    planta=random.choice(PLANTAS),
                    endemica=bool(random.randint(0,1)))
        facts.append(fact)

for idx, hap0 in enumerate(haps):
    for hap1 in haps[idx+1:]:
        edge = Edge(random.randint(1, 10), hap0, hap1)
        edges.append(edge)






#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




