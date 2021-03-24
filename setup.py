from setuptools import setup

setup(
    name='network-destruction',
    version='0.0.1',
    author='Tancredi Orlando',
    url='https://github.com/turlando/network-destruction',

    classifiers=[
        ('License :: OSI Approved :: '
         'GNU Affero General Public License v3 or later (AGPLv3+)')
    ],

    python_requires='>=3.6, <4',

    package_dir={'network_destruction': 'network_destruction'},
    packages=['network_destruction'],

    install_requires=[
        'networkx==2.5',
        'scipy==1.6.1',
        'matplotlib==3.3.4'
    ]
)
