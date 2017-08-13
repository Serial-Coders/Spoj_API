# SpojPI: Spoj Programming Interface
[![AUR](https://img.shields.io/aur/license/yaourt.svg?style=plastic)]() [![AUR](https://img.shields.io/badge/python-2.6%2C%202.7%2C%203.3%2C%203.4%2C%203.5%2C%203.6-blue.svg?style=plastic)]() [![Waffle.io](https://img.shields.io/waffle/label/evancohen/smart-mirror/in%20progress.svg)]()

A high functional programming interface for spoj.

Can do a huge variety of stuff with the spoj, be it the fetching problem from SPOJ, submitting it, comparing our profile with other, or it be getting the info of the user, or it may it be the changing the information of the user, all this is packed with SpojPI. A small, lightweight, easy to use, day-by-day getting better is all set.

```python
>>> from spoj import user, problem
>>> u = User('lord_poseidon')
>>> u.name
'Nimit Bhardwaj'
>>> u.school
'National Institute of Technology, Hamirpur'
>>> u.login('<password here>')
>>> u.editFirstName('Luffy') #change in spoj profile
>>> u.name
'Luffy Bhardwaj'
>>> p = Problem('TEST')
>>> p.problemName
'Life, the Universe, and Everything'
>>> p.tags
['#basic', '#tutorial', '#ad-hoc-1']
>>> status = u.submitProblem(p, 'TEST.c') #TEST.c is in present directory
>>> status
(0, 'Accepted')
```
A very simple and easy to understand code

## Features
You wanna know the features man, I hope that this brief sample of code provide you some info of the features you can built the list, so let be formal, here is the list of the features:
* Easy to use
* Highly functional
* Can do any thing programmability, which u can do yourself
* Sorry, can do much more than a you can do with Spoj now
* Good documentation

## Installation
To install SpojPI just write
`pip install spojpi`
... or if you like the old-fashion way of installing from source you can also do
`python setup.py install`

## Documentation

The documentation can be found [here](), you can refer to it, its not too big, easy to understand, RTFM.

## How to Contribute
If you like this project well, and you like to contribute, then its very easy,

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a Contributor Friendly tag for issues that should be ideal for people who are not very familiar with the codebase yet.
2. Fork the repository on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS.


