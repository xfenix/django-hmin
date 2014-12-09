# -*- coding: utf-8 -*-
import codecs
from os.path import abspath, dirname, join
from django.test import SimpleTestCase
from django.test.utils import override_settings

from hmin import minify


data_path = abspath(join(dirname(__file__), 'data'))
load_file = lambda name: codecs.open(
    '%s.html' % join(data_path, name), encoding='utf-8'
).read()


class MinifyTestCase(SimpleTestCase):
    def test_data_htmls(self):
        examples = [
            'habrahabr',
            'lenta',
            'gazeta',
            'youtube',
        ]
        for example in examples:
            print 'Test file %s' % example
            self.assertEqual(
                minify(load_file(example)), load_file(example + '_min')
            )
