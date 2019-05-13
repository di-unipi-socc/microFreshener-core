from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='microanalyser',
      version='1.1',
      description='',
      long_description=readme(),
      url='',
      include_package_data=True,
      author='Davide Neri',
      author_email='davide.neri@di.unipi.it',
      license='MIT',
      packages=['microanalyser'],
      install_requires=[
          'ruamel.yaml','tosca-parser'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'microanalyserm=microanalyser.command_line:main',
        ],
    },
)
