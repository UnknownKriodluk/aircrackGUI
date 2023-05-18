from setuptools import setup

setup(
    name='aircrackgui_bykriod',
    version='1.0',
    author='UnknownKriodluk',
    author_email='vitalka19203@gmail.com',
    description='GUI для AirCrack-ng',
    url='https://github.com/UnknownKriodluk/aircrackGUI/',
    packages=['aircrackgui'],
    install_requires=[
        'tkinter',
        'subprocess',
        'os_sys',
        'platform',
        're',
        'time',
    ],
)
