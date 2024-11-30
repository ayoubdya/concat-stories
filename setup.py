"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

requirements = [
  package for package in open('requirements.txt').readlines() if package != ''
]

setup(
  name='concat-stories',
  version='0.1.0',
  description='Concatenate Snapchat stories.',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='Ayoub Dya',
  author_email='ayoubdya@gmail.com',
  url='https://github.com/ayoubdya/concat-stories',
  entry_points={
    'console_scripts': [
      'concat-stories = src.app:main',
    ],
  },
  packages=find_packages(),
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
