from conans import ConanFile
from conans.tools import download, unzip, replace_in_file, check_sha256
import os
import shutil
from conans import CMake, ConfigureEnvironment

class DuktapeConan(ConanFile):
    name = "duktape"
    version = "2.0.0"
    settings = "os", "arch", "compiler", "build_type"
    exports = "CMakeLists.txt"
    generators = "cmake"
    url="http://github.com/TyRoXx/conan-duktape"
    license="MIT"
    source_root = "duktape-2.0.0"

    def source(self):
        zip_name = "duktape-2.0.0.tar.xz"
        download("http://duktape.org/%s" % zip_name, zip_name)
        check_sha256(zip_name, "e07bc1178225218a281de9f73f555390743dd805bafd5396229c69a16f740c4d")
        self.run("cmake -E tar xf %s" % zip_name)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.source_root)

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir _build")
        configure_command = 'cd _build && cmake ../%s %s' % (self.source_root, cmake.command_line)
        self.run(configure_command)
        self.run("cd _build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy(pattern="*.h", dst="include", src="%s/src" % self.source_root, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="_build", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="_build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["duktape"]
