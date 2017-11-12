#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans import ConfigureEnvironment
from conans.errors import ConanException
import os

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
    exports_sources = "CMakeLists.txt"
    exports = "FindFreetype.cmake"
    requires = "libpng/1.6.34@bincrafters/stable", "bzip2/1.0.6@lasote/stable"
    source_url = "http://downloads.sourceforge.net/project/freetype/freetype2/{0}".format(version)

    def requirements(self):
        if self.options.with_harfbuzz:
            self.requires.add("harfbuzz/1.6.3@bincrarfters/testing")

    def config(self):
        del self.settings.compiler.libcxx 
        #if self.settings.compiler == "Visual Studio" and self.options.shared:
        #    raise ConanException("The lib CMakeLists.txt does not support creation of SHARED libs")

    def source(self):
        archive_file = '{0}-{1}.tar.gz'.format(self.name, self.version)
        source_file = '{0}/{1}'.format(self.source_url, archive_file)
        tools.get(source_file)

        os.rename('{0}-{1}'.format(self.name, self.version), 'sources')

        tools.replace_in_file(os.path.join('sources','CMakeLists.txt'),
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

        cmake.configure(source_dir="..", build_dir="build")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindFreetype.cmake", ".", ".")

        # Copy the license files
        self.copy("LICENSE.TXT", dst="licenses", src="%s/docs" % self.folder, ignore_case=True, keep_path=False)
        self.copy("FLT.TXT", dst="licenses", src="%s/docs" % self.folder, ignore_case=True, keep_path=False)
        self.copy("GPLv2.TXT", dst="licenses", src="%s/docs" % self.folder, ignore_case=True, keep_path=False)

        #self.copy("*", dst="include", src='include', keep_path=True, symlinks=True)
        #self.copy(pattern="*.h", dst="include", src="%s/include" % self.folder, keep_path=True)
        #self.copy("*freetype*.lib", dst="lib", keep_path=False)
        # UNIX
        if not self.options.shared:
            self.copy(pattern="*.a", dst="lib", keep_path=False)
        else:
            #self.copy(pattern="*.dll*", dst="bin", src="%s/bin" % self.folder, keep_path=False)
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            libname = "freetyped"
        else:
            libname = "freetype"

        self.cpp_info.libs = [libname]
        self.cpp_info.includedirs.append(os.path.join("include","freetype2"))
