import unittest


target = __import__("dpkg_status_parser")
parser = target.dpkg_parser


class MyTestCase(unittest.TestCase):
    def test_one_package(self):
        string = """Package: vim
Depends: vim-common (= 2:8.0.1453-1ubuntu1.1), vim-runtime (= 2:8.0.1453-1ubuntu1.1), libacl1 (>= 2.2.51-8), libc6 (>= 2.15), libgpm2 (>= 1.20.7), libpython3.6 (>= 3.6.5), libselinux1 (>= 1.32), libtinfo5 (>= 6)
Suggests: ctags, vim-doc, vim-scripts
Description: Vi IMproved - enhanced vi editor
 Vim is an almost compatible version of the UNIX editor Vi.
 .
 Many new features have been added: multi level undo, syntax
 highlighting, command line history, on-line help, filename
 completion, block operations, folding, Unicode support, etc.
 .
 This package contains a version of vim compiled with a rather
 standard set of features.  This package does not provide a GUI
 version of Vim.  See the other vim-* packages if you need more
 (or less)."""
        result = len(parser(string))
        self.assertEqual(result, 9)  # 1 package + 8 dependencies

    def test_my_package(self):
        string = """Package: package1
Depends: package2
Description: A normal package
 It does something

Package: package2
Description: A package that is normal


"""
        result = parser(string)
        expected = {
            "package1": {
                "depends": ["package2"],
                "reverse-depends": [],
                "description": ["A normal package", " It does something"],
            },
            "package2": {
                "depends": [],
                "reverse-depends": ["package1"],
                "description": ["A package that is normal"],
            },
        }
        self.assertDictEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
