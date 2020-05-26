from setuptools import setup

setup(
    name='flask_blog',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask', 'PyYAML', 'PyYAML', 'dotenv', 'python-dotenv'
    ],
)
