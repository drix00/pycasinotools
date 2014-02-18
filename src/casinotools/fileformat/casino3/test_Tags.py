#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2378 $"
__svnDate__ = "$Date: 2011-06-20 15:45:48 -0400 (Mon, 20 Jun 2011) $"
__svnId__ = "$Id: test_Tags.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest

# Third party modules.
from pkg_resources import resource_filename #@UnresolvedImport
from nose.plugins.attrib import attr

# Local modules.
import casinotools.fileformat.casino3.Tags as Tags

# Globals and constants variables.

@attr('ignore')
class TestTags(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        filepath = resource_filename(__name__, "../../testData/casino3.x/SiSubstrateThreeLines_Points.sim")
        self.file = open(filepath, 'rb')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_createTagWithFiller(self):
        tagIDs = []
        tagIDs.append("V3.1.3.4")
        tagIDs.append("V3.1.3.7")
        tagIDs.append("%SAVE_HEADER%")

        tagLenght = 15
        filler = '%'

        tagRefs = []
        tagRefs.append("V3.1.3.4%%%%%%%")
        tagRefs.append("V3.1.3.7%%%%%%%")
        tagRefs.append("%SAVE_HEADER%%%")

        for tagID, tagRef in zip(tagIDs, tagRefs):
            tag = Tags.createTagWithFiller(tagID, tagLenght, filler)

            self.assertEquals(tagRef, tag)

        tagLenght = 10
        tagRefs = []
        tagRefs.append("V3.1.3.4%%")
        tagRefs.append("V3.1.3.7%%")
        tagRefs.append("%SAVE_HEADER%")

        for tagID, tagRef in zip(tagIDs, tagRefs):
            tag = Tags.createTagWithFiller(tagID, tagLenght, filler)

            self.assertEquals(tagRef, tag)

        #self.fail("Test if the testcase is working.")

    def test_limitedSearchTag(self):
        searchLength = 1024

        tagIDs = []
        tagIDs.append("V3.1.3.4")
        tagIDs.append("V3.1.3.7")
        tagIDs.append("%SAVE_HEADER%")

        isTagFounds = []
        isTagFounds.append(False)
        isTagFounds.append(False)
        isTagFounds.append(True)

        for tagID, isTagFoundRef in zip(tagIDs, isTagFounds):
            isTagFound = Tags.limitedSearchTag(self.file, tagID, searchLength)

            self.assertEquals(isTagFoundRef, isTagFound)

        #self.fail("Test if the testcase is working.")

    def test_searchTag(self):
        tagIDs = []
        tagIDs.append("V3.1.3.4")
        tagIDs.append("V3.1.3.7")
        tagIDs.append("%SAVE_HEADER%")

        isTagFounds = []
        isTagFounds.append(False)
        isTagFounds.append(False)
        isTagFounds.append(True)

        for tagID, isTagFoundRef in zip(tagIDs, isTagFounds):
            isTagFound = Tags.searchTag(self.file, tagID)

            self.assertEquals(isTagFoundRef, isTagFound)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__': #pragma: no cover
    import logging, nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.runmodule()
