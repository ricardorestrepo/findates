from distutils.core import setup

setup(
    name='FinDates',
    version='0.2',
    description = 'Dealing with dates in finance',
    author='Artem Frolov (Amelanche Inc.)',
    author_email='findates@artemfrolov.fastmail.fm',
    packages=['findates', 'findates.test'],
    license='OSI Approved',
    long_description=open('README.txt').read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial',
    ]
)

