import os
from autotest.client import test, utils

class ubuntu_qrt_kernel_security(test.test):
    version = 1

    def initialize(self):
        self.job.require_gcc()

    def setup(self, tarball='ubuntu_qrt_kernel_security.tar.bz2'):
        tarball = utils.unmap_url(self.bindir, tarball, self.tmpdir)
        utils.extract_tarball_to_dir(tarball, self.srcdir)
        print(utils.system_output('head %s/scripts/bzr.log' % self.srcdir, retain_output=True))

    def run_once(self, test_name):
        scripts = os.path.join(self.srcdir, 'scripts')
        os.chdir(scripts)

        if test_name == 'setup':
            return

        cmd = 'python ./%s -v' % test_name
        self.results = utils.system_output(cmd, retain_output=True)


# vi:set ts=4 sw=4 expandtab:
