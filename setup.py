from setuptools import setup, find_packages

setup(
    name='wallet_pay',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Max Palehin',
    author_email='maksim.wsem@gmail.com',
    description='A Python client for the pay.wallet.tg API',
    license='MIT',
    keywords='WalletPay API Client',
)
