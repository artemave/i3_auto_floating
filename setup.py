from setuptools import setup, find_packages

setup(
    name='sway_auto_floating',
    version='1.0',
    description='Remember floating state of Sway windows and automatically set it when a new window of the same app is created.',
    author='Artem Avetisyan',
    packages=find_packages(),
    license='MIT',
    url='https://github.com/artemave/sway_auto_floating',
    include_package_data=True,
    install_requires=[
        'i3ipc>=2.2.1',
    ],
    entry_points={
        'console_scripts': [
            'sway_toggle_floating = sway_auto_floating.toggle_floating:main',
            'sway_auto_floating = sway_auto_floating.auto_floating:main',
        ],
    },
)
