from setuptools import setup, find_packages

setup(
    name='koalanlp',
    version='1.0.1',
    description='Python wrapper for KoalaNLP',
    author='Bugeun Kim',
    author_email='cd4209@gmail.com',
    url='https://nearbydelta.github.io/py-koalanlp',
    install_requires=[
        "Cython>=0.27.3", "pyjnius>=1.1.1", "jip>=0.9.13"
    ],
    packages=find_packages(exclude=["docs"]),
    keywords=['korean', 'natural language processing', 'koalanlp', 'sentence', 'parser', 'tagger'],
    python_requires='>=3.5',
    package_data={},
    zip_safe=False,
    license="MIT",
    project_urls={
        "Issue Tracker": "https://github.com/nearbydelta/py-koalanlp/issues",
        "Source Code": "https://github.com/nearbydelta/py-koalanlp",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Korean',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic'
    ]
)