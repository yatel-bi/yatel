#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

# ===============================================================================
# DOC
# ===============================================================================

"""yatel.dom module tests"""


# ===============================================================================
# IMPORTS
# ===============================================================================
import numpy as np
from yatel import stats
from scipy import stats as statsbis
from yatel.tests.core import YatelTestCase

# ===============================================================================
# VALIDATE TESTS
# ===============================================================================


class TestStats(YatelTestCase):

    def setUp(self):
        super(TestStats, self).setUp()
        self.warr = np.array([edge.weight for edge in self.nw.edges()])
        self.warrenv = {}
        for env in self.nw.enviroments():
            self.warrenv[env] = np.array([
                edge.weight for edge in self.nw.edges_by_enviroment(env)
            ])
        self.places = 2

    def tearDown(self):
        super(TestStats, self).tearDown()
        self.warr = None
        self.places = None

    def test_average(self):
        orig = np.average(self.warr)
        rs = stats.average(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            orig = np.average(self.warrenv[env])
            rs = stats.average(self.nw, env)
            if np.isnan(orig) or np.isnan(rs):
                self.assertTrue(np.isnan(orig) and np.isnan(rs))
            else:
                self.assertAlmostEqual(orig, rs, self.places)

    def test_median(self):
        orig = np.median(self.warr)
        rs = stats.median(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            orig = np.median(self.warrenv[env])
            rs = stats.median(self.nw, env)
            if np.isnan(orig) or np.isnan(rs):
                self.assertTrue(np.isnan(orig) and np.isnan(rs))
            else:
                self.assertAlmostEqual(orig, rs, self.places)

    def test_min(self):
        orig = np.min(self.warr)
        rs = stats.min(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            arr = len(self.warrenv[env])
            if arr != 0:
                orig = np.min(self.warrenv[env])
                rs = stats.min(self.nw, env)
                if np.isnan(orig) or np.isnan(rs):
                    self.assertTrue(np.isnan(orig) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(orig, rs, self.places)
            else:
                print "El array es de longitud cero"

    def test_max(self):
        orig = np.max(self.warr)
        rs = stats.max(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            arr = len(self.warrenv[env])
            if arr != 0:
                orig = np.max(self.warrenv[env])
                rs = stats.max(self.nw, env)
                if np.isnan(orig) or np.isnan(rs):
                    self.assertTrue(np.isnan(orig) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(orig, rs, self.places)
            else:
                print "El array es de longitud cero"

    def test_amin(self):
        orig = np.amin(self.warr)
        rs = stats.amin(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            arr = len(self.warrenv[env])
            if arr != 0:
                orig = np.amin(self.warrenv[env])
                rs = stats.amin(self.nw, env)
                if np.isnan(orig) or np.isnan(rs):
                    self.assertTrue(np.isnan(orig) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(orig, rs, self.places)
            else:
                print "El array es de longitud cero"

    def test_amax(self):
        orig = np.amax(self.warr)
        rs = stats.amax(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            arr = len(self.warrenv[env])
            if arr != 0:
                orig = np.amax(self.warrenv[env])
                rs = stats.amax(self.nw, env)
                if np.isnan(orig) or np.isnan(rs):
                    self.assertTrue(np.isnan(orig) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(orig, rs, self.places)
            else:
                print "El array es de longitud cero"

    def test_sum(self):
        orig = np.sum(self.warr)
        rs = stats.sum(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            orig = np.sum(self.warrenv[env])
            rs = stats.sum(self.nw, env)
            if np.isnan(orig) or np.isnan(rs):
                self.assertTrue(np.isnan(orig) and np.isnan(rs))
            else:
                self.assertAlmostEqual(orig, rs, self.places)

    def test_var(self):
        orig = np.var(self.warr)
        rs = stats.var(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            orig = np.var(self.warrenv[env])
            rs = stats.var(self.nw, env)
            if np.isnan(orig) or np.isnan(rs):
                self.assertTrue(np.isnan(orig) and np.isnan(rs))
            else:
                self.assertAlmostEqual(orig, rs, self.places)

    def test_std(self):
        orig = np.std(self.warr)
        rs = stats.std(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            orig = np.std(self.warrenv[env])
            rs = stats.std(self.nw, env)
            if np.isnan(orig) or np.isnan(rs):
                self.assertTrue(np.isnan(orig) and np.isnan(rs))
            else:
                self.assertAlmostEqual(orig, rs, self.places)

    def test_variation(self):
        orig = statsbis.variation(self.warr)
        rs = stats.variation(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            orig = statsbis.variation(self.warrenv[env])
            rs = stats.variation(self.nw, env)
            if np.isnan(orig) or np.isnan(rs):
                self.assertTrue(np.isnan(orig) and np.isnan(rs))
            else:
                self.assertAlmostEqual(orig, rs, self.places)

    def test_range(self):
        orig = np.amax(self.warr) - np.amin(self.warr)
        rs = stats.range(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            arr = len(self.warrenv[env])
            if arr != 0:
                orig = np.amax(self.warrenv[env]) - np.amin(self.warrenv[env])
                rs = stats.range(self.nw, env)
                if np.isnan(orig) or np.isnan(rs):
                    self.assertTrue(np.isnan(orig) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(orig, rs, self.places)
            else:
                print "El array es de longitud cero"

    def test_kurtosis(self):
        orig = statsbis.kurtosis(self.warr)
        rs = stats.kurtosis(self.nw)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            orig = statsbis.kurtosis(self.warrenv[env])
            rs = stats.kurtosis(self.nw, env)
            if np.isnan(orig) or np.isnan(rs):
                self.assertTrue(np.isnan(orig) and np.isnan(rs))
            else:
                self.assertAlmostEqual(orig, rs, self.places)

    def test_percentiles(self):
        orig = np.percentile(self.warr, 25)
        rs = stats.percentile(self.nw, 25)
        self.assertAlmostEqual(orig, rs, self.places)
        for env in self.nw.enviroments():
            arr = len(self.warrenv[env])
            if arr != 0:
                orig = np.percentile(self.warrenv[env], 25)
                rs = stats.percentile(self.nw, 25, env)
                if np.isnan(orig) or np.isnan(rs):
                    self.assertTrue(np.isnan(orig) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(orig, rs, self.places)
            else:
                print "El array es de longitud cero"

    def test_mode(self):
        rs = stats.mode(self.nw)
        aux = 0
        cont = 0
        moda = -1
        self.warr.sort()
        for i in range(0, len(self.warr)-1):
            if (self.warr[i] == self.warr[i+1]):
                cont = cont + 1
                if cont >= aux:
                    aux = cont
                    moda = self.warr[i]
            else:
                cont = 0
        self.assertAlmostEqual(moda, rs, self.places)
        for env in self.nw.enviroments():
            arr = len(self.warrenv[env])
            if arr != 0:
                for i in range(0, len(self.warrenv[env])-1):
                    if (self.warr[i] == self.warrenv[i+1]):
                        cont = cont + 1
                        if cont >= aux:
                            aux = cont
                            moda = self.warr[i]
                    else:
                        cont = 0
                rs = stats.mode(self.nw, env)
                if np.isnan(moda) or np.isnan(rs):
                    self.assertTrue(np.isnan(moda) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(moda, rs, self.places)
            else:
                print "El array es de longitud cero"

    def test_weights2array(self):
        orig = self.warr
        rs = stats.weights2array(self.nw.edges())
        self.assertEqual(orig.all(), rs.all())

    def test_env2weightarray(self):
        orig = self.warr
        rs = stats.env2weightarray(self.nw)
        self.assertEqual(orig.all(), rs.all())
        for env in self.nw.enviroments():
            orig = self.warrenv[env]
            rs = stats.env2weightarray(self.nw, env)
            arr = len(self.warrenv[env])
            if arr != 0:
                orig = self.warrenv[env]
                rs = stats.env2weightarray(self.nw, env)
                if np.isnan(orig) or np.isnan(rs):
                    self.assertTrue(np.isnan(orig) and np.isnan(rs))
                else:
                    self.assertAlmostEqual(orig, rs, self.places)
            print "El array es de longitud cero"


# ===============================================================================
# MAIN
# ===============================================================================

if __name__ == "__main__":
    print(__doc__)
