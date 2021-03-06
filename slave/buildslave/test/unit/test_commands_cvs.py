import os

from twisted.trial import unittest
from twisted.python import runtime

from buildslave.test.fake.runprocess import Expect
from buildslave.test.util.sourcecommand import SourceCommandTestMixin
from buildslave.commands import cvs

class TestCVS(SourceCommandTestMixin, unittest.TestCase):

    def setUp(self):
        self.setUpCommand()

    def tearDown(self):
        self.tearDownCommand()

    def test_simple(self):
        self.patch_getCommand('cvs', 'path/to/cvs')
        self.clean_environ()
        self.make_command(cvs.CVS, dict(
            workdir='workdir',
            mode='copy',
            revision=None,
            cvsroot=':pserver:anoncvs@anoncvs.NetBSD.org:/cvsroot',
            cvsmodule='htdocs',
        ))

        exp_environ = dict(PWD='.', LC_MESSAGES='C')
        expects = [
            Expect([ 'clobber', 'workdir' ],
                self.basedir)
                + 0,
            Expect([ 'clobber', 'source' ],
                self.basedir)
                + 0,
            Expect([ 'path/to/cvs', '-d', ':pserver:anoncvs@anoncvs.NetBSD.org:/cvsroot',
                     '-z3', 'checkout', '-d', 'source', 'htdocs' ],
                self.basedir,
                sendRC=False, timeout=120, usePTY=False)
                + 0,
            Expect([ 'copy', 'source', 'workdir'],
                self.basedir)
                + 0,
        ]
        self.patch_runprocess(*expects)

        d = self.run_command()
        d.addCallback(self.check_sourcedata,
                ":pserver:anoncvs@anoncvs.NetBSD.org:/cvsroot\nhtdocs\nNone\n")
        return d

