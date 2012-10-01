from setuptools import setup, find_packages

description="""
DB-API2 connection pool for Django (for postgresql, mysql and sqlite)
"""

setup(
    name = "djorm-ext-pool",
    version = '0.4.0',
    url = 'https://github.com/niwibe/djorm-ext-pool',
    license = 'BSD',
    platforms = ['OS Independent'],
    description = description.strip(),
    author = 'Andrey Antukh',
    author_email = 'niwi@niwi.be',
    maintainer = 'Andrey Antukh',
    maintainer_email = 'niwi@niwi.be',
    packages = find_packages(),
    include_package_data = False,
    install_requires = [
        'sqlalchemy >= 0.7.5',
    ],
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
