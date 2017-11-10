from conans import ConanFile
from conans.errors import ConanException
from conans.tools import download, unzip, replace_in_file
import os
import shutil
from conans import CMake, ConfigureEnvironment

class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.8.1"
    folder = "freetype-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_harfbuzz": [True, False] }
    default_options = "shared=False", "fPIC=True", "with_harfbuzz=False"
    generators = "cmake"
    url="http://github.com/bincrafters/conan-freetype"
    license="MIT"
    exports = "FindFreetype.cmake"
    requires = "libpng/1.6.34@bincrafters/stable", "bzip2/1.0.6@lasote/stable"

    def requirements(self):
        self.requires.add("harfbuzz/1.6.3@bincrarfters/testing")

    def config(self):
        del self.settings.compiler.libcxx 
        #if self.settings.compiler == "Visual Studio" and self.options.shared:
        #    raise ConanException("The lib CMakeLists.txt does not support creation of SHARED libs")

    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        download("http://downloads.sourceforge.net/project/freetype/freetype2/{0}/{1}".format(self.version, zip_name), zip_name)
        unzip(zip_name)
        replace_in_file("freetype-%s/CMakeLists.txt" % self.version,
                        "project(freetype)",
                        """project(freetype)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")
        replace_in_file("freetype-%s/CMakeLists.txt" % self.version,
                        'if (WIN32 AND NOT MINGW AND BUILD_SHARED_LIBS)\n' +
                        '  message(FATAL_ERROR "Building shared libraries on Windows needs MinGW")\n' +
                        'endif ()\n',
                        '')


    def build(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = "On"

        cmake.definitions["WITH_ZLIB"] = "On"
        cmake.definitions["WITH_PNG"] = "On"
        cmake.definitions["WITH_HarfBuzz"] = self.options.with_harfbuzz

        cmake.configure(source_dir="freetype-%s" % self.version)
        cmake.build()
        cmake.install()

    def build_with_make(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.options.fPIC:
            env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
        else:
            env_line = env.command_line
            
        custom_vars = "LIBPNG_LIBS=0 BZIP2_LIBS=0" # Trick: This way it didn't look for system libs and take the env variables from env_line
                
        self.run("cd %s" % self.folder)
        
        self.output.warn(env_line)
        if self.settings.os == "Macos": # Fix rpath, we want empty rpaths, just pointing to lib file
            old_str = "-install_name \$rpath/"
            new_str = "-install_name "
            replace_in_file("%s/builds/unix/configure" % self.folder, old_str, new_str)

        ## NEEDS FIXING FOR HARFBUZZ
        configure_command = 'cd %s && %s ./configure --with-harfbuzz=no %s' % (self.folder, env_line, custom_vars)
        self.output.warn("Configure with: %s" % configure_command)
        self.run(configure_command)
        self.run("cd %s && %s make" % (self.folder, env_line))


    def package(self):
        self.copy("FindFreetype.cmake", ".", ".")

        # Copy the license files
        self.copy("LICENSE.TXT", dst="licenses", src="%s/docs" % self.folder, ignore_case=True, keep_path=False)
        self.copy("FLT.TXT", dst="licenses", src="%s/docs" % self.folder, ignore_case=True, keep_path=False)
        self.copy("GPLv2.TXT", dst="licenses", src="%s/docs" % self.folder, ignore_case=True, keep_path=False)

        self.copy(pattern="*.h", dst="include", src="%s/include" % self.folder, keep_path=True)
        self.copy("*freetype*.lib", dst="lib", keep_path=False)
        # UNIX
        if not self.options.shared:
            self.copy(pattern="*.a", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.dll*", dst="bin", src="%s/bin" % self.folder, keep_path=False)
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            libname = "freetyped"
        else:
            libname = "freetype"
        self.cpp_info.libs = [libname]
