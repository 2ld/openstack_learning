#!/usr/bin/env python
# coding=utf-8
import oslo_messaging
from oslo_config import cfg

cfg.CONF(default_config_files=['/etc/nova/nova.conf'])

def get_transport():
    transport = oslo_messaging.get_notification_transport(cfg.CONF)
    return transport

def get_notification_listener(transport, targets, endpoints):
    listener = oslo_messaging.get_notification_listener(transport,
                                                        targets,
                                                        endpoints)
    return listener

def convert_notification_format():
    pass
