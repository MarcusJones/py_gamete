from setuptools import setup, find_packages
package_list = find_packages()
for p in package_list:
    print(p)
setup(
    packages=find_packages()
)

setup(name='gamete',
      version='1.1',
      description='Description here',
      author='Marcus Jones',
      author_email='a',
      url='none',
      packages=package_list,
     )

