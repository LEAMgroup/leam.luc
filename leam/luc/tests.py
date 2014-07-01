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

        # Integration tests for LUCDriverSet
        ztc.ZopeDocFileSuite(
            'LUCDriverSet.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for LUCFolder
        ztc.ZopeDocFileSuite(
            'LUCFolder.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for LUCDriver
        ztc.ZopeDocFileSuite(
            'LUCDriver.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for LUCProjection
        ztc.ZopeDocFileSuite(
            'LUCProjection.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for LUCScenario
        ztc.ZopeDocFileSuite(
            'LUCScenario.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for DriverFolder
        ztc.ZopeDocFileSuite(
            'DriverFolder.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ProjectionFolder
        ztc.ZopeDocFileSuite(
            'ProjectionFolder.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ScenarioFolder
        ztc.ZopeDocFileSuite(
            'ScenarioFolder.txt',
            package='leam.luc',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
