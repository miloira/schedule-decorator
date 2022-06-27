#-*-coding:utf-8-*-
from setuptools import setup

with open("README.md","r",encoding="utf-8") as f:
    desc = f.read()

setup(
    name="schedule-decorator",
    version="2.1.2",
    description="A wonderful decorator package from schedule!",
    long_description_content_type="text/markdown",
    long_description=desc,
    author="Msky",
    author_email="690126048@qq.com",
    url="https://github.com/miloira/schedule-decorator",
    packages=["schedule_decorator"],
    install_requires=["schedule"]
)