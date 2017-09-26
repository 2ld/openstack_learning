#!/usr/bin/env python
# coding=utf-8


class TestEndpoint(object):

    def test(self, ctx, arg):
        print 'TestEndpoint the arg is %s' % arg


class MambaEndpoint(object):

    def get_name(self, ctx, arg):
        if isinstance(arg, dict):
            return arg.get('name', None)
        else:
            return 'Mamba'
