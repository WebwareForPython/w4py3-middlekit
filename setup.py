import setuptools

with open('webware/MiddleKit/Properties.py') as f:
    properties = {}
    exec(f.read(), properties)
    version = properties['version']
    version = '.'.join(map(str, version[:3])) + '.'.join(version[3:])
    description = properties['synopsis']

with open('README.md') as fh:
    long_description = fh.read()


setuptools.setup(
    name='Webware-for-Python-MiddleKit',
    version=version,
    author='cito, jhildeb, nl et al.',
    author_email='nl@mnet-online.de',
    description=description,
    #install_requires=['Webware-for-Python>=3.0.0'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='database orm',
    url='https://github.com/nlgio/w4py3-middlekit/',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable', #@@pre-relase 
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'webware.plugins': [
            'MiddleKit = webware.MiddleKit',
        ]
    }
) 
