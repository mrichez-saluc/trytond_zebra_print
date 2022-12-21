# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class ZebraPrintTestCase(ModuleTestCase):
    'Test Zebra Print module'
    module = 'zebra_print'


del ModuleTestCase
