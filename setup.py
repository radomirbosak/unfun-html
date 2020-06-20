# -*- coding: utf-8 -*-
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'unfun_html', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    author='Radomír Bosák',
    author_email='radomir.bosak@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Website parsing resilient to website changes',
    download_url='https://github.com/radomirbosak/unfun_html/archive/' \
                 + about['__version__'] + '.tar.gz',
    entry_points={
        'console_scripts': [
            'unfun-html = unfun_html.main:main'
        ]
    },
    include_package_data=True,
    install_requires=[],
    keywords=['unfun_html'],
    name='unfun_html',
    packages=['unfun_html'],
    url='https://github.com/radomirbosak/unfun_html',
    version=about['__version__'],
)
