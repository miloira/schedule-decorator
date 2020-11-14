#-*-coding:utf-8-*-
from setuptools import setup

with open("README.rst","r",encoding="utf-8") as f:
    desc = f.read()

setup(
    name="schedule_decorator",
    version="2.1.0",
    description="A wonderful decorator package from schedule!",
    long_description=desc,
    author="Kenny",
    author_email="690126048@qq.com",
    url="https://github.com/zhangmingming-chb",
    packages=["schedule_decorator"],
    install_requires=["schedule"]
)