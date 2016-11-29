# -*- coding: utf-8 -*-
## @package setup
#
#  setup utility package.
#  @author      tody
#  @date        2015/08/14

from setuptools import setup, find_packages
from som_cm import __author__, __version__, __license__

setup(
        name = 'som_cm',
        version = __version__,
        description = 'Simple python demos of Data-driven Color Manifolds [Nguyen et al. 2015].',
        license = __license__,
        author = __author__,
        url = 'https://github.com/tody411/SOM-ColorManifolds.git',
        packages = find_packages(),
        install_requires = ['docopt'],
        )

