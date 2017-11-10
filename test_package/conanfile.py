from conans import ConanFile, tools, CMake
from conans import GCC, CMake
import os

class DefaultNameConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        lib_dir_src = 'lib' if self.settings.os != 'Windows' else 'bin'
        self.copy("*.dll", dst="bin", src=lib_dir_src)
        self.copy("*.dylib*", dst="bin", src=lib_dir_src)
        self.copy('*.so*', dst='bin', src=lib_dir_src)

    def test(self):
        self.output.warn("conan: " + self.conanfile_directory)
        bin_dir = os.path.join(os.getcwd(), "bin")
        os.chdir(bin_dir)
        with tools.environment_append({"LD_LIBRARY_PATH": bin_dir, "DYLD_LIBRARY_PATH": bin_dir}):
            fontfile = os.path.join(self.conanfile_directory, 'OpenSans-Bold.ttf')
            self.run(".{sep}test_package {fontfile} 'lasote!' > file.txt".format(fontfile=fontfile, sep=os.sep))
