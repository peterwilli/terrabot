from setuptools import setup

setup(
    name='terrabot',
    version='0.1.0',    
    description='Automatically swap (non-native) tokens',
    url='https://github.com/peterwilli/terrabot',
    author='Peter Willemsen',
    author_email='peter@codebuffet.co',
    license='MIT',
    packages=['terrabot'],
    install_requires=[
        'terra-sdk>=2.0.5',
        'python-box>=6.0.2'
    ]
)
