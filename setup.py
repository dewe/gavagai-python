from setuptools import setup
setup(
    name='Gavagai',
    description='A Gavagai API helper library.',
    version='0.1',
    packages=['gavagai'],
    license='The MIT License (MIT)',
    install_requires=[
        'requests>=2.6.0,<3.0',
        'urllib3',
        'ndg-httpsclient',
    ]
)