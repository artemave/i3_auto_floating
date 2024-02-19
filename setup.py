from setuptools import setup, find_packages

setup(
    name='i3_auto_floating',
    version='1.3',
    description='Remember floating state of i3wm windows and automatically set it when a new window of the same app is created.',
    author='Artem Avetisyan',
    packages=find_packages(),
    license='MIT',
    url='https://github.com/artemave/i3_auto_floating',
    include_package_data=True,
    install_requires=[
        'i3ipc>=2.2.1',
    ],
    entry_points={
        'console_scripts': [
            'i3_toggle_floating = i3_auto_floating.toggle_floating:main',
            'i3_auto_floating = i3_auto_floating.auto_floating:main',
        ],
    },
)
