#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <jbc.develop@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a WISKEY in return Juan BC

#===============================================================================
# IMPORTS
#===============================================================================

import os, random, collections, hashlib, time, pprint

from yatel import db, db3, dom

import numpy as np


#===============================================================================
# PRE CONFIG
#===============================================================================

path = os.path.dirname(os.path.abspath(__file__))
peewee_path = os.path.join(path, "data", "bench_pewee.db")
sa_path = os.path.join(path, "data", "bench_sa.db")

if os.path.exists(peewee_path):
    os.remove(peewee_path)
if os.path.exists(sa_path):
    os.remove(sa_path)


#===============================================================================
# BENCH DEC
#===============================================================================

benchs = collections.OrderedDict()
funcs = []

def bench(times=1):
    def _bench(func):
        funcs.append((func, times))
        return func
    return _bench


def run():
    for func, times in funcs:
        results = []
        for _ in range(times):
            start = time.time()
            func()
            end = time.time()
            results.append(end-start)
        benchs[func.__name__] = np.average(results)


#===============================================================================
# CREATE SOME NETWORKS
#===============================================================================

def create_network():
    choices = {
        int: lambda: random.randint(1, 100),
        float: lambda: random.randint(1, 100) + random.random(),
        str: lambda: hashlib.sha1(str(random.random)).hexdigest(),
        bool: lambda: bool(random.randint(0, 1)),
    }

    haps = []
    for idx in range(random.randint(10, 50)):
        name = "haplotype_" + str(idx)
        attrs = {}
        for jdx, func in enumerate(sorted(choices.values())):
            attrs["attr_" + str(jdx)] = func()
        haps.append(dom.Haplotype(name, **attrs))

    facts = []
    for _ in range(random.randint(899, 900)):
        hap_id = random.choice(haps).hap_id
        attrs = {}
        for jdx, func in enumerate(sorted(choices.values())):
            attrs["attr_" + str(jdx)] = func()
        facts.append(dom.Fact(hap_id, b=1, c=2, k=2))

    edges = []
    for _ in range(random.randint(10, 50)):
        weight = choices[float]()
        hap_0 = random.choice(haps).hap_id
        hap_1 = random.choice(haps).hap_id
        while hap_1 == hap_0:
            hap_1 = random.choice(haps).hap_id
        edges.append(dom.Edge(weight, hap_0, hap_1))

    return (haps, facts, edges)

#===============================================================================
# THE NETWORK
#===============================================================================

haps, facts, edges = create_network()

print len(haps) + len(facts) + len(edges)

#===============================================================================
# CREATE THE two db
#===============================================================================

peewee_db = None
sa_db = None

@bench()
def create_peewee():
    conn = db.YatelConnection("sqlite", name=peewee_path)
    conn.init_with_values(haps, facts, edges)

@bench()
def create_sa():
    conn = db3.YatelNetwork("sqlite", dbname=sa_path, create=True)
    map(conn.add_element, haps)
    map(conn.add_element, facts)
    map(conn.add_element, edges)
    conn.end_creation()

@bench()
def connect_peewee():
    global peewee_db
    peewee_db = db.YatelConnection("sqlite", name=peewee_path)
    peewee_db.init_yatel_database()

@bench()
def connect_sa():
    global sa_db
    sa_db = db3.YatelNetwork("sqlite", dbname=sa_path)

@bench(100)
def iter_haplotypes_peewee():
    list(peewee_db.iter_haplotypes())

@bench(100)
def iter_haplotypes_sa():
    list(sa_db.iter_haplotypes())

@bench(100)
def iter_facts_peewee():
    list(peewee_db.iter_facts())

@bench(100)
def iter_facts_sa():
    list(sa_db.iter_facts())

@bench(100)
def iter_edges_peewee():
    list(peewee_db.iter_edges())

@bench(100)
def iter_edges_sa():
    list(sa_db.iter_edges())

@bench(100)
def haplotype_by_id_peewee():
    for hap in haps:
        peewee_db.haplotype_by_id(hap.hap_id)

@bench(100)
def haplotype_by_id_sa():
    for hap in haps:
        sa_db.haplotype_by_id(hap.hap_id)

@bench(1)
def enviroment_peewee():
    for fact in facts:
        env = dict(fact.items_attrs())
        list(peewee_db.enviroment(**env))

@bench(1)
def enviroment_sa():
    for fact in facts:
        env = dict(fact.items_attrs())
        list(sa_db.enviroment(env))

@bench(1)
def edges_enviroment_peewee():
    for fact in facts:
        env = dict(fact.items_attrs())
        list(peewee_db.edges_enviroment(**env))
        break

@bench(1)
def edgest_enviroment_sa():
    for fact in facts:
        env = dict(fact.items_attrs())
        list(sa_db.edges_enviroment(env))
        break

@bench(100)
def fact_attributes_names_peewee():
    list(peewee_db.fact_attributes_names())

@bench(100)
def fact_attributes_names_sa():
    list(sa_db.fact_attributes_names())

@bench(100)
def fact_attribute_values_peewee():
    for an in peewee_db.fact_attributes_names():
        list(peewee_db.fact_attribute_values(an))

@bench(100)
def fact_attribute_values_sa():
    for an in sa_db.fact_attributes_names():
        list(sa_db.fact_attribute_values(an))

@bench(100)
def facts_by_haplotype_peewee():
    for hap in haps:
        list(peewee_db.facts_by_haplotype(hap))

@bench(100)
def facts_by_haplotype_sa():
    for hap in haps:
        list(sa_db.facts_by_haplotype(hap))

@bench(100)
def minmax_edges_peewee():
    peewee_db.minmax_edges()

@bench(100)
def minmax_edges_sa():
    sa_db.minmax_edges()


#===============================================================================
# MAIN
#===============================================================================

def main():
    run()
    for k, v in benchs.items():
        print "{} -> {}".format(k, v)

if __name__ == "__main__":
    main()