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
import tempfile
import shutil
import filecmp
import os
import logging

# Third party modules.

# Local modules.
from casinotools.scripting.casino3 import BatchFile
from  casinotools.utilities.path import get_current_module_path

# Globals and constants variables.

class TestBatchFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        if os.name == 'posix':
            self.scriptFilepathRef = get_current_module_path(__file__, "../../../testData/scripting/casino3/BatchFilePosix.bat")
        else:
            self.scriptFilepathRef = get_current_module_path(__file__, "../../../testData/scripting/casino3/BatchFile.bat")
        self.temporaryPath = tempfile.mkdtemp()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.temporaryPath)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_createFile(self):
        basename = "TestCasinoBatchFile"
        batchFile = BatchFile.BatchFile()
        batchFile.setPath(self.temporaryPath)
        batchFile.setScriptPath("scripts")
        batchFile.setBasename(basename)
        scriptFilenames = ["S%i.txt" % (i) for i in xrange(1, 6, 1)]
        batchFile.setScriptFilenames(scriptFilenames, len(scriptFilenames), 0)

        batchFile.createFile()
        batchFilepath = batchFile._generateBatchFilepath()
        logging.debug(batchFilepath)

        linesRef = open(self.scriptFilepathRef, 'rb').readlines()
        lines = open(batchFilepath, 'rb').readlines()

        for lineRef, line in zip(linesRef, lines):
            self.assertEquals(lineRef, line)

        self.assertTrue(filecmp.cmp(batchFilepath, self.scriptFilepathRef, shallow=True))

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':    #pragma: no cover
    import nose
    logging.getLogger().setLevel(logging.DEBUG)
    nose.main()
