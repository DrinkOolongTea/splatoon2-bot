import setuptools

setuptools.setup(name='nanobot-plugin-splatoon2tools',  # 包名
      version='1.2.0',  # 版本号
      description='splatoon2 tools bot',
      long_description='splatoon2 tools bot',
      author='DrinkOolongTea',
      author_email='sh.elsyion@qq.com',
      url='https://github.com/DrinkOolongTea/splatong2-bot',
      install_requires=["lxml",
      "Pillow","nonebot2","nonebot-adapter-onebot"],
      license='GNU General Public License v3.0',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ],
      )
