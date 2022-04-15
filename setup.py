import setuptools

setup(name='splatoon2_tools',  # 包名
      version='1.0.0',  # 版本号
      description='splatoon2 tools bot',
      long_description=long_description,
      author='DrinkOolongTea',
      author_email='sh.elsyion@qq.com',
      url='https://github.com/DrinkOolongTea/splatong2-bot',
      install_requires=["lxml",
      "Pillow"],
      license='GNU General Public License v3.0',
      packages=setuptools.find_packages(),
      data_files=[('images',['resource/*.png']),
      'fonts',['resource/*.TTF']]
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
      ],
      )