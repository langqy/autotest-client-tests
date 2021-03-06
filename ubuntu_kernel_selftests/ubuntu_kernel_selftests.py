#
#
import os
import platform
from autotest.client                        import test, utils

class ubuntu_kernel_selftests(test.test):
    version = 1

    def install_required_pkgs(self):
        arch   = platform.processor()
        series = platform.dist()[2]

        pkgs = [
            'build-essential', 'git',
        ]
        gcc = 'gcc' if arch in ['ppc64le', 'aarch64', 's390x'] else 'gcc-multilib'
        pkgs.append(gcc)

        cmd = 'apt-get install --yes --force-yes ' + ' '.join(pkgs)
        self.results = utils.system_output(cmd, retain_output=True)

    def initialize(self):
        self.install_required_pkgs()
        self.job.require_gcc()

    def setup(self):
        os.chdir(self.srcdir)
        series = platform.dist()[2]

        # Use a local repo for manual testing. If it does not exist, then clone from the master
        # repository.
        #
        repo = os.environ['HOME'] + '/ubuntu/ubuntu-%s' % series
        if os.path.exists(repo) is True:
            cmd = 'git clone -q %s linux' % repo
            utils.system(cmd)

        # No local repository, so clone from the master repo.
        #
        if os.path.exists('linux') is False:
            cmd = 'git clone https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/%s linux' % series
            utils.system(cmd)
            # tweak sleep wake alarm time to 30 seconds as 5 is a bit too small
            #
            fn = 'linux/tools/testing/selftests/breakpoints/step_after_suspend_test.c'
            if os.path.exists(fn):
               cmd = 'sed -i "s/tv_sec = 5;/tv_sec = 30;/" ' + fn
               utils.system(cmd)
            # currently disable step_after_suspend_test as this breaks ssh'd login
            # connections to the test VMs and real H/W
            fn = 'linux/tools/testing/selftests/breakpoints/Makefile'
            if os.path.exists(fn):
                cmd = 'sed -i "s/TEST_PROGS += step_after_suspend_test/# TEST_PROGS += step_after_suspend_test/" ' + fn
                utils.system(cmd)

    def run_once(self, test_name):
        os.chdir(self.srcdir)
        cmd = "sudo make -C linux/tools/testing/selftests/%s all run_tests" % test_name
        utils.system(cmd)

# vi:set ts=4 sw=4 expandtab syntax=python:
