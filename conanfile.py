#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.8.1"
    description = "FreeType is a freely available software library to render fonts."
    url="http://github.com/bincrafters/conan-freetype"
    homepage = "https://www.freetype.org"
    license="BSD"
    exports = ["LICENSE.md", "FindFreetype.cmake"]
    exports_sources = ["CMakeLists.txt", "freetype.pc.in"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_harfbuzz": [True, False] }
    default_options = "shared=False", "fPIC=True", "with_harfbuzz=False"
    requires = "libpng/[>=1.6.34]@bincrafters/stable", "bzip2/[>=1.0.6]@conan/stable"
    source_url = "http://downloads.sourceforge.net/project/freetype/freetype2/{0}".format(version)
    source_subfolder = "sources"

    def requirements(self):
        if self.options.with_harfbuzz:
            self.requires.add("harfbuzz/[>=1.7.1]@bincrafters/stable")

    def config(self):
        del self.settings.compiler.libcxx

    def source(self):
        archive_file = '{0}-{1}.tar.gz'.format(self.name, self.version)
        source_file = '{0}/{1}'.format(self.source_url, archive_file)      
        tools.get(source_file)

        os.rename('{0}-{1}'.format(self.name, self.version), self.source_subfolder)

        tools.replace_in_file(os.path.join(self.source_subfolder, 'CMakeLists.txt'),
                              'if (WIN32 AND NOT MINGW AND BUILD_SHARED_LIBS)\n' +
                              '  message(FATAL_ERROR "Building shared libraries on Windows needs MinGW")\n' +
                              'endif ()\n',
                              '')

    def fetch_hb(self):
        return

    def build(self):
        cmake = CMake(self)
        #cmake.verbose = True
        cmake.definitions["PROJECT_VERSION"] = self.version
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = "On"
        
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

        cmake.definitions["WITH_ZLIB"] = "On"
        cmake.definitions["WITH_PNG"] = "On"
        cmake.definitions["WITH_HarfBuzz"] = self.options.with_harfbuzz

        if self.options.with_harfbuzz:
            self.fetch_hb()

        cmake.configure(build_dir="build")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindFreetype.cmake")

        # Copy the license files
        self.copy("%s/docs/FTL*" % self.source_subfolder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy("%s/docs/GPLv2*" % self.source_subfolder, dst="licenses", ignore_case=True, keep_path=False)
        self.copy("%s/docs/LICENSE*" % self.source_subfolder, dst="licenses", ignore_case=True, keep_path=False)

        self.copy("freetype.pc", dst=os.path.join('lib','pkgconfig'), ignore_case=True, keep_path=True)
        self.copy("freetype2.pc", dst=os.path.join('lib','pkgconfig'), ignore_case=True, keep_path=True)

        #self.copy("*", dst="include", src='include', keep_path=True, symlinks=True)
        #self.copy(pattern="*.h", dst="include", src="%s/include" % self.source_subfolder, keep_path=True)
        #self.copy("*freetype*.lib", dst="lib", keep_path=False)
        # UNIX
        if not self.options.shared:
            self.copy(pattern="*.a", dst="lib", keep_path=False)
        else:
            #self.copy(pattern="*.dll*", dst="bin", src="%s/bin" % self.source_subfolder, keep_path=False)
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            libname = "freetyped"
        else:
            libname = "freetype"

        self.cpp_info.libs = [libname]
        self.cpp_info.includedirs.append(os.path.join("include","freetype2"))
