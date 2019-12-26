from setuptools import setup

tests_require = ['tox', 'pytest']

setup(
    name='func_prototypes',
    version='0.4',
    description='library which helps people constrain python functions by type.',
    url='https://github.com/andrewguy9/func_prototypes',
    author='andrew thomson',
    author_email='athomsonguy@gmail.com',
    license='MIT',
    packages=['func_prototypes'],
    entry_points = {
      'console_scripts': [
        ],
    },
    tests_require=tests_require,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False)
