"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

requirements = [
  package for package in open('requirements.txt').readlines() if package != ''
]

version = {}
with open("src/version.py") as fp:
  exec(fp.read(), version)

setup(
  name='concat-stories',
  version=version['__version__'],
  description='Concatenate Snapchat stories.',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='Ayoub Dya',
  author_email='ayoubdya@gmail.com',
  url='https://github.com/ayoubdya/concat-stories',
  package_dir={'': 'src'},
  entry_points={
    'console_scripts': [
      'concat-stories = app:main',
    ],
  },
  packages=find_packages(where='src'),
  install_requires=requirements,
  keywords='concat-stories',
  license='MIT',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
