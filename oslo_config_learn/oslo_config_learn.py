#!/usr/bin/env python
# coding=utf-8

from oslo_config import cfg

opt_group = cfg.OptGroup(name='keystone_authtoken',
                         title='keyston')
opts = [
    cfg.StrOpt('auth_uri',
                default='',
                help='vcpu_pin_set'),

    cfg.StrOpt('auth_url',
               default='',
               help='reserved_host_memory_mb'),
    cfg.StrOpt('auth_type',
               default='',
               help='reserved_host_memory_mb')
]

CONF = cfg.CONF
CONF.register_group(opt_group)
CONF.register_opts(opts, group=opt_group)

if __name__ == "__main__":
    CONF(default_config_files=['nova.conf'])
    print(CONF.keystone_authtoken.auth_type)
