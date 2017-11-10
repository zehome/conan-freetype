from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="freetype:shared", pure_c=True) 
    filtered_builds = []
    for settings, options in builder.builds:
        if settings["compiler"] != "Visual Studio" or options["freetype:shared"] == False:
             filtered_builds.append([settings, options])
    builder.builds = filtered_builds
    builder.run()