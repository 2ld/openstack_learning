#!/usr/bin/env python
# coding=utf-8
import oslo_messaging
from oslo_config import cfg
import messaging
from endpoint import TestEndpoint

# TRANSPORT_URL = 'rabbit://openstack:78f6f54a69@10.0.0.3/'
TOPIC = 'notifications'
cfg.CONF(default_config_files=['/etc/nova/nova.conf'])

listener = None


def start():
    # Init transport
    transport = messaging.get_transport()
    # Init endpint
    endpoints = [
        TestEndpoint()
    ]
    # Init target
    targets = [
        oslo_messaging.Target(topic=TOPIC)
    ]
    listener = messaging.get_notification_listener(transport,
                                                   targets,
                                                   endpoints)
    listener.start()
    listener.wait()


def stop():
    listener.stop()
