# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 13.05.2019
"""


def runtests():
    import sys
    import pytest
    from os import environ
    from os.path import dirname, join
    cfg_path = join(dirname(dirname(dirname(__file__))), 'setup.cfg')

    args = sys.argv[1:]
    if not args or args[0].startswith('-'):
        args += ['--pyargs', 'cykooz.testing']
    args = ['-c', cfg_path] + args
    environ['IS_TESTING'] = 'True'
    pytest.main(args)
