from setuptools import setup

setup(
    name='trackerino',
    version='0.1',
    description='Simple time tracker',
    url='http://github.com/decaruju/trackerino',
    author='decaruju',
    author_email='julien.decarufel@gmail.com',
    license='MIT',
    packages=['trackerino'],
    zip_safe=False,
    scripts=['bin/trk'],
)
