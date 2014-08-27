import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import leam.luc

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['leam.luc'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              leam.luc)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='leam.luc',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='leam.luc.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for DriverSet
        ztc.ZopeDocFileSuite(
            'DriverSet.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for LUC
        ztc.ZopeDocFileSuite(
            'LUC.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Driver
        ztc.ZopeDocFileSuite(
            'Driver.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Projection
        ztc.ZopeDocFileSuite(
            'Projection.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Scenario
        ztc.ZopeDocFileSuite(
            'Scenario.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Drivers
        ztc.ZopeDocFileSuite(
            'Drivers.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Projections
        ztc.ZopeDocFileSuite(
            'Projections.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Scenarios
        ztc.ZopeDocFileSuite(
            'Scenarios.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
