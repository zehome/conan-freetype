[![Build Status](https://travis-ci.org/bincrafters/conan-freetype.svg)](https://travis-ci.org/bincrafters/conan-freetype)


# conan-freetype

[Conan.io](https://conan.io) package for [freetype library](https://www.freetype.org/)

The packages generated with this **conanfile** can be found in [conan.io].

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload freetype/2.8.1@bincrafters/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install freetype/2.8.1@bincrafters/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    freetype/2.8.1@bincrafters/stable

    [options]
    freetype:shared=True # False
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
