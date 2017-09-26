#!/usr/bin/env python
# coding=utf-8
import oslo_messaging
import event as convert


class TestEndpoint(object):

    def __init__(self):
        self.event_converter = convert.setup_events()

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        notification = self._convert_to_old_notification_format('info',
                                                                ctxt,
                                                                publisher_id,
                                                                event_type,
                                                                payload,
                                                                metadata)
        data = self.process_notification(notification)
        print 'data is %s' % data
        return oslo_messaging.NotificationResult.REQUEUE

    def _convert_to_old_notification_format(self,
                                            priority,
                                            ctxt,
                                            publisher_id,
                                            event_type,
                                            payload,
                                            metadata):
        notification = {'priority': priority,
                        'payload': payload,
                        'event_type': event_type,
                        'publisher_id': publisher_id}
        notification.update(metadata)
        for k in ctxt:
            notification['_context_' + k] = ctxt[k]
        return notification

    def process_notification(self, notification):
        return self.event_converter.to_event(notification)
