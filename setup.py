from setuptools import find_packages, setup

package_name = 'censys_event_analytics'
requirements = [
    "numpy",
    "pandas",
    "matplotlib",
]
setup(name=package_name,
      version='1.0',
      description='Used to investigate squirrely events',
      author='Sarah West',
      author_email='sarah.irene.west@gmail.com',
      packages=find_packages(exclude=("test",)),
      install_requires=requirements,
      python_requires=">=3.8",
      package_data={'event_analytics': ['data-dump/*.csv']},
)