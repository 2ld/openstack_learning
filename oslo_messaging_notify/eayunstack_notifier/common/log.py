#!/usr/bin/env python
# coding=utf-8
import logging
from logging.config import dictConfig

LOG_PATH = '/var/log/eayunstack_notifier/eayunstack_notifier.log'


class LOGManager(object):

    def get_logger(self):
        dict_config = dict(
            version=1,
            formatters={
                'f': {'format':
                      '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
                },
            handlers={
                'StreamHandler': {'class': 'logging.StreamHandler',
                                  'formatter': 'f',
                                  'level': logging.INFO},
                'FileHandler': {
                    'class': 'logging.FileHandler',
                    'formatter': 'f',
                    'level': logging.INFO,
                    'filename': '%s' % LOG_PATH
                }
                },
            root={
                'handlers': ['StreamHandler', 'FileHandler'],
                'level': logging.DEBUG,
                },
            )
        dictConfig(dict_config)
        logger = logging.getLogger('test_log')
        return logger


logManager = LOGManager()
LOG = logManager.get_logger()
