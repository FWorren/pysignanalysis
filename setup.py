try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = "pysignanalysis"

config = {
    'description': 'Signal analysis toolbox for Hilbert Huang Transform',
    'author': 'Geir Kulia, Joar Molvaer, Fredrik Worren',
    'url': 'https://github.com/FWorren/pysignanalysis',
    'download_url': 'https://github.com/FWorren/pysignanalysis',
    'author_email': 'freworr@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'scipy', 'numpy', 'matplotlib'],
    'packages': [NAME],
    'scripts': [],
    'name': NAME
}

setup(**config)
