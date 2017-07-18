#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.skip import SkipTest

# Local modules.
import casinotools.fileformat.Tags as Tags
from casinotools.utilities.path import is_bad_file

# Globals and constants variables.

class TestTags(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        filepath = resource_filename(__name__, "../../test_data/casino3.x/SiSubstrateThreeLines_Points.sim")
        if is_bad_file(filepath):
            raise SkipTest
        self.file = open(filepath, 'rb')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assertTrue(True)

    def test_createTagWithFiller(self):
        tagIDs = []
        tagIDs.append(b"V3.1.3.4")
        tagIDs.append(b"V3.1.3.7")
        tagIDs.append(b"%SAVE_HEADER%")

        tagLenght = 15
        filler = b'%'

        tagRefs = []
        tagRefs.append(b"V3.1.3.4%%%%%%%")
        tagRefs.append(b"V3.1.3.7%%%%%%%")
        tagRefs.append(b"%SAVE_HEADER%%%")

        for tagID, tagRef in zip(tagIDs, tagRefs):
            tag = Tags.createTagWithFiller(tagID, tagLenght, filler)

            self.assertEqual(tagRef, tag)

        tagLenght = 10
        tagRefs = []
        tagRefs.append(b"V3.1.3.4%%")
        tagRefs.append(b"V3.1.3.7%%")
        tagRefs.append(b"%SAVE_HEADER%")

        for tagID, tagRef in zip(tagIDs, tagRefs):
            tag = Tags.createTagWithFiller(tagID, tagLenght, filler)

            self.assertEqual(tagRef, tag)

        #self.fail("Test if the testcase is working.")

    def test_limitedSearchTag(self):
        searchLength = 1024

        tagIDs = []
        tagIDs.append(b"V3.1.3.4")
        tagIDs.append(b"V3.1.3.7")
        tagIDs.append(b"%SAVE_HEADER%")

        isTagFounds = []
        isTagFounds.append(False)
        isTagFounds.append(False)
        isTagFounds.append(True)

        for tagID, isTagFoundRef in zip(tagIDs, isTagFounds):
            isTagFound = Tags.limitedSearchTag(self.file, tagID, searchLength)

            self.assertEqual(isTagFoundRef, isTagFound)

        #self.fail("Test if the testcase is working.")

    def test_searchTag(self):
        tagIDs = []
        tagIDs.append(b"V3.1.3.4")
        tagIDs.append(b"V3.1.3.7")
        tagIDs.append(b"%SAVE_HEADER%")

        isTagFounds = []
        isTagFounds.append(False)
        isTagFounds.append(False)
        isTagFounds.append(True)

        for tagID, isTagFoundRef in zip(tagIDs, isTagFounds):
            isTagFound = Tags.searchTag(self.file, tagID)

            self.assertEqual(isTagFoundRef, isTagFound)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
