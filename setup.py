from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md', encoding='UTF-8').read()


setup(
    name='koalanlp',
    version='2.1.5-SNAPSHOT',
    description='Python wrapper for KoalaNLP',
    long_description=long_description,
    author='koalanlp',
    url='https://koalanlp.github.io/python-support',
    install_requires=["py4j~=0.10", "requests~=2.22"],
    packages=find_packages(exclude=["docs", "tests", "doc_source", "scripts"]),
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
