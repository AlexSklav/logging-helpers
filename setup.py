import sys

import setuptools as st

sys.path.insert(0, '.')
import version

st.setup(name='logging-helpers',
         version=version.getVersion(),
         description='Add description here.',
         keywords='',
         author='Christian Fobel',
         author_email='christian@fobel.net',
         url='https://github.com/wheeler-microfluidics/logging-helpers',
         license='BSD',
         packages=['logging_helpers'],
         install_requires=['path-helpers'],
         # Install data listed in `MANIFEST.in`
         include_package_data=True)
