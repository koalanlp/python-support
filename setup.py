from setuptools import setup, find_packages

setup(
    name='koalanlp',
    version='2.0.0',
    description='Python wrapper for KoalaNLP',
    author='koalanlp',
    url='https://koalanlp.github.io/python-support',
    install_requires=[
        "Cython~=0.29", "pyjnius~=1.1.3", "jip~=0.9.13"
    ],
    packages=find_packages(exclude=["docs", "tests", "doc_source"]),
    keywords=['korean', 'natural language processing', 'koalanlp', '한국어 처리', '한국어 분석',
              '형태소', '의존구문', '구문구조', '개체명', '의미역'],
    python_requires='>=3.5',
    package_data={},
    zip_safe=False,
    license="MIT",
    project_urls={
        "Issue Tracker": "https://github.com/koalanlp/python-support/issues",
        "Source Code": "https://github.com/koalanlp/python-support",
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
