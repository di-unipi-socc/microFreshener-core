from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='microtosca',
      version='0.1',
      description='',
      long_description=readme(),
      url='',
      include_package_data=True,
      author='Davide Neri',
      author_email='davide.neri@di.unipi.it',
      license='MIT',
      packages=['microtosca'],
      install_requires=[
          'ruamel.yaml','tosca-parser'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],)
