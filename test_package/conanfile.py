from conans import ConanFile, CMake, RunEnvironment, tools
import os

class DefaultNameConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            fontfile = os.path.join(self.conanfile_directory, 'OpenSans-Bold.ttf')
            args = '{fontfile} \'lasote!\' > file.txt'.format(fontfile=fontfile)
            test_binary = os.path.join("bin","test_package")

            if self.settings.os == "Macos":
                test_binary = "DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), test_binary)
            elif self.settings.os != "Windows":
                test_binary = "LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), test_binary)

            self.run("%s %s" % (test_binary, args))