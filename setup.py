from setuptools import setup

setup(
    name='func_prototypes',
    version='0.5',
    author='Andrew Thomson',
    author_email='athomsonguy@gmail.com',
    packages=['func_prototypes'],
    url='https://github.com/andrewguy9/func_prototypes',
    license='MIT',
    description='library which helps people constrain python functions by type.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 2.7',
    ],
)
