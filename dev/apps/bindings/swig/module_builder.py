"""GPSTk module __init__.py generator and build finisher.

Usage:
    python module_builder.py
    This runs the program and builds to the gpstk folder in the current directory.

    python module_builder.py ~/.local/lib/python2.7/site-packages
    This runs the program and builds to ~/.local/lib/python2.7/site-packages/
"""

import argparse
import os
import shutil
import sys


# Any object that is exactly a string in this list will be ignored
ignore_exact = [
'FFData'
''
]

# Any object that contains a string in this list will be ignored
ignore_patterns = [
'swigregister',
'gpstk_pylib',
'ObsIDInitializer',
'Stream',
'EngNav_',
'OrbElem_',
'Position_',
'TimeTag_',
'RinexObsHeader_',
'VectorBase'
]


def should_be_added(name):
    for pattern in ignore_patterns:
        if pattern in name:
            return False
    for pattern in ignore_exact:
        if pattern == name:
            return False
    if name[:1] == '_':
        return False
    else:
        return True


def main(arg='.'):
    # Create __init__.py file
    import gpstk_pylib
    namespace = dir(gpstk_pylib)
    out_file = open('__init__.py', 'w')
    out_file.write('"""The GPS Toolkit - an open source library to the satellite navigation community.\n"""\n')
    out_file.write('### This file is AUTO-GENERATED by module_builder.py. ###\n\n')
    for x in namespace:
        if should_be_added(x):
            out_file.write('from gpstk_pylib import ')
            out_file.write(x)
            out_file.write('\n')

    # Create gpstk folder, move things into it
    out_dir = 'gpstk/'
    files_to_move = ['gpstk_pylib.py', '__init__.py']

    # we don't know extension of library file, so search the directory:
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if '_gpstk_pylib' in f:
            files_to_move.append(f)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for f in files_to_move:
        if os.path.exists(f):
            os.rename(f, out_dir + f)
        # adds pyc file if it exists:
        if os.path.exists(f + 'c'):
            os.rename(f + 'c', out_dir + f + 'c')

    if len(sys.argv) >= 2:
        if (sys.argv[1])[-1] != '/' and (sys.argv[1])[-1] != '\\':
            sys.argv[1] = sys.argv[1] + '/'
        out = sys.argv[1] + out_dir
        shutil.rmtree(out)
        shutil.move(out_dir, out)


if __name__ == '__main__':
    main()