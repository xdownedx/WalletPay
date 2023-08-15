from setuptools import setup, find_packages

setup(
    name='WalletPay',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Max Palehin',
    author_email='maksim.wsem@gmail.com',
    url='https://github.com/xdownedx/WalletPay',
    long_description=open('Readme.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
