from setuptools import setup, find_packages

setup(
    name='ansible-manager',
    packages=find_packages(),
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ansible-manager=cli:cli
    ''',
)