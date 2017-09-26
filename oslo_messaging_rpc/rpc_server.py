#!/usr/bin/env python
# coding=utf-8
from oslo_config import cfg
import oslo_messaging
import endpoints as ep
import time

cfg.CONF(default_config_files=['/etc/nova/nova.conf'])


def get_transport():
    return oslo_messaging.get_transport(cfg.CONF)


def main():
    transport = get_transport()
    target = oslo_messaging.Target(topic='test', server='server1')
    endpoints = [
        ep.TestEndpoint(),
        ep.MambaEndpoint()
    ]
    server = oslo_messaging.get_rpc_server(transport,
                                           target,
                                           endpoints)
    try:
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server")

    server.stop()
    server.wait()


if __name__ == '__main__':
    main()
