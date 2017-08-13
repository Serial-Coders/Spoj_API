from setuptools import setup

requires = ['requests>=2.18.2', 'bs4>=0.0.1', 'beautifulsoup4>=4.6.0', 'lxml>=3.8.0']

desc = '''
A high functional programming interface for spoj.

Can do a huge variety of stuff with the spoj, be it the fetching problem from SPOJ, submitting it, comparing our profile with other, or it be getting the info of the user, or it may it be the changing the information of the user, all this is packed with SpojPI. A small, lightweight, easy to use, day-by-day getting better is all set.

'''

setup(name='spojpi',
        version='0.1.1',
        description='An easy to use python package for using the functionallity of spoj programatically',
        long_description=desc,
        author='Nimit Bhardwaj',
        author_email='nimitbhardwaj@gmail.com',
        url='https://github.com/nimitbhardwaj/SpojPI',
        packages=['spoj'],
        license='GPL-3.0',
        install_requires=requires,
        classifiers=[
                    'Development Status :: 2 - Pre-Alpha',
                    'Intended Audience :: Developers',
                    'Programming Language :: Python',
                    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
                   ],
        )
