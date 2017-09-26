#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="Eayunstack_notification",
    version="0.1",
    packages=find_packages(),
    author="ArmStrong",
    author_email="vpbvmw651078@gmail.com",
    description="Eayunstack Notifilter Tool",
    entry_points={
        'console_scripts': [
            'eayunstack-notifier = eayunstack_notifier.notification_listener:start',
             ]})
