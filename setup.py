import sys

import setuptools as st
import versioneer


st.setup(name='logging-helpers',
         version=versioneer.get_version(),
         cmdclass=versioneer.get_cmdclass(),
         description='Add description here.',
         keywords='',
         author='Christian Fobel',
         author_email='christian@fobel.net',
         url='https://github.com/wheeler-microfluidics/logging-helpers',
         license='BSD',
         packages=['logging_helpers'],
         # Install data listed in `MANIFEST.in`
         include_package_data=True)
