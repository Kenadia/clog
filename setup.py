import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='clog',
    version='0.0.1',
    author='Ken Schiller',
    author_email='kenschiller@gmail.com',
    description='Python logging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Kenadia/clog',
    packages=setuptools.find_packages(),
    install_requires=[],
)
