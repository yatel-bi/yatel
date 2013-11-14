#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.db module tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random

from yatel import db
from yatel.tests.core import YatelTestCase


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestFunctions(YatelTestCase):

    def test_enviroments(self):
        desc = self.nw.describe()
        fact_attrs = desc["fact_attributes"].keys()
        for size in xrange(0, len(fact_attrs)):
            filters = set()
            while len(filters) < size:
                f = random.choice(fact_attrs)
                if f != "hap_id":
                    filters.add(f)
            list(self.nw.enviroments(list(filters)))




    def test_copy(self):
        anw = db.YatelNetwork(engine="memory", mode=db.MODE_WRITE)
        db.copy(self.nw, anw)
        anw.confirm_changes()
        for method in ["haplotypes", "facts", "edges"]:
            nw_values = getattr(self.nw, method)()
            anw_values = getattr(anw, method)()
            self.assertSameUnsortedContent(nw_values, anw_values)
        self.assertEquals(self.nw.describe(), anw.describe())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
