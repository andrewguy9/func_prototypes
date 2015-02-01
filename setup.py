from setuptools import setup

tests_require = ['tox', 'pytest']

setup(name='prototypes',
      version='0.1',
      description='library which helps people constrain python functions by type.',
      url='http://github.com/andrewguy9/prototypes',
      author='andrew thomson',
      author_email='athomsonguy@gmail.com',
      license='MIT',
      packages=['prototypes'],
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points = {
        'console_scripts': [
          ],
      },
      zip_safe=False)
