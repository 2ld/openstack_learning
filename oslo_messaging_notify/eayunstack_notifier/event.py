#!/usr/bin/env python
# coding=utf-8

import fnmatch
import yaml
import jsonpath_rw
from common.log import LOG as logger


FILE_PATH = ('/root/armstrong/python_scripts/oslo_messaging_as'
             '/eayunstack_notifier/etc/event_definitions.yaml')


def setup_events():
    if FILE_PATH is not None:
        logger.info("Event Definitions configuration file: %s"
                    % FILE_PATH.split('/')[-1])

        with open(FILE_PATH) as cf:
            config = cf.read()
        try:
            events_config = yaml.safe_load(config)
        except yaml.YAMLError as err:
            if hasattr(err, 'problem_mark'):
                mark = err.problem_mark
                errmsg = ("Invalid YAML syntax in Event Definitions file "
                          "%(file)s at line: %(line)s, column: %(column)s."
                          % dict(file=FILE_PATH.split('/')[-1],
                                 line=mark.line + 1,
                                 column=mark.column + 1))
            else:
                errmsg = ("YAML error reading Event Definitions file: %s"
                          % FILE_PATH.split('/')[-1])
            logger.error(errmsg)
            raise
        else:
            return EventConverter(events_config)
    else:
        logger.error("No Event Definitions configuration file found!")


class EventConverter(object):
    def __init__(self, events_config):
        self.definitions = [EventDefinition(event_def) for event_def
                            in reversed(events_config)]

    def to_event(self, notification_body):
        event_type = notification_body['event_type']
        edef = None
        for d in self.definitions:
            if d.match_type(event_type):
                edef = d
                break
        if edef is None:
            logger.info("Dropping Notification %s" % event_type)
            return None
        logger.info("Event Notification is about to convert : %s from"
                    " Module EventConverter." % event_type)
        return edef.to_event(notification_body)


class EventDefinition(object):
    def __init__(self, definition_cfg):
        self.traits = dict()
        self.include_types = []
        self.cfg = definition_cfg
        self.invalid_keys = {"event_type", "Action"}

        event_type = definition_cfg['event_type']
        self.include_types.append(event_type)
        for t in self.include_types:
            logger.info("Monitored resources from "
                        "event definition yaml file: %s" % t.split('.')[0])

        for trait_name in self.exclude_keys(self.cfg, self.invalid_keys):
            self.traits[trait_name] = TraitDefinition(
                trait_name, definition_cfg[trait_name])

    def exclude_keys(self, d, keys):
        return {x: d[x] for x in d if x not in keys}

    def match_type(self, event_type):
        for t in self.include_types:
            if fnmatch.fnmatch(event_type, t):
                return True
            else:
                return False

    def to_event(self, notification_body):
        event_type = notification_body['event_type']
        logger.info("Event_type from notification_body %s from"
                    " Module EventDefnition." % event_type)
        traits = (self.traits[t].to_trait(notification_body)
                  for t in self.traits)
        trait_dict = {}
        try:
            for trait in traits:
                trait_dict[trait.name] = trait.value or None
        except Exception as err:
            logger.error("The trait error is: %s" % err)

        trait_dict['Action'] = self.cfg['Action']
        return trait_dict


class TraitDefinition(object):
    def __init__(self, name, trait_cfg):
        self.cfg = trait_cfg
        self.name = name

        if 'fields' not in trait_cfg:
            logger.error("Required fields in trait definition not "
                         "specified:'%s'" % 'fields', self.cfg)
            return None

        fields = trait_cfg['fields']
        try:
            self.fields = jsonpath_rw.parse(fields)
            logger.info("Jsonpath_rw's fields: %s" % self.fields)
        except Exception as e:
            logger.error("Parse error in JSONPath specification "
                         "'%(jsonpath)s' for %(trait)s: %(err)s"
                         % dict(jsonpath=fields, trait=name, err=e))

    def to_trait(self, notification_body):
        values = [match for match in self.fields.find(notification_body)]
        value_list = [match.value or '' for match in values]
        value = ''.join(value_list)
        return Trait(self.name, value)


class Trait(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return ('%s, %s') % (self.name, self.value)
    __repr__ = __str__
