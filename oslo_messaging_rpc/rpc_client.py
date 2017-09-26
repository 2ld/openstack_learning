#!/usr/bin/env python
# coding=utf-8
from oslo_config import cfg
import oslo_messaging
import time

cfg.CONF(default_config_files=['/etc/nova/nova.conf'])


def get_transport():
    return oslo_messaging.get_transport(cfg.CONF)


def main():
    transport = get_transport()
    target = oslo_messaging.Target(topic='test', server='server1')
    client = oslo_messaging.RPCClient(transport, target)
    arg = {'name': 'ArmStrong Liu'}
    ctxt = {"application": "rpc-client", "time": time.ctime()}
    arg_name = client.call(ctxt, 'get_name', arg=arg)
    print arg_name


if __name__ == '__main__':
    main()
