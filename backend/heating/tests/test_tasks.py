# -*- coding: utf-8 -*-

import logging

import pytest

from pilotwire_controller.client import PilotwireModesInconsistent

from .. import tasks


class FakeControllerProxy:

    TEST_TYPE = 'undefined'

    def check_status(self):
        if self.TEST_TYPE == 'not_active':
            return 'not_active_test'
        else:
            return 'active'

    @property
    def modes(self):
        pass

    @modes.setter
    def modes(self, _):
        if self.TEST_TYPE == 'modes_inconsistent':
            raise PilotwireModesInconsistent("Inconsistent test")
        else:
            return


@pytest.mark.parametrize(['test_type', 'level', 'message'], [
    ('all_ok', 'INFO', "Modes set on pilotwire controller : {}"),
    ('not_active', 'ERROR',
     "Failed to connect to pilotwire controller : not_active_test"),
    ('modes_inconsistent', 'ERROR', "Inconsistent test"),
])
@pytest.mark.django_db
def test_setpilotwire(monkeypatch, caplog, test_type, level, message):
    FakeControllerProxy.TEST_TYPE = test_type
    monkeypatch.setattr(tasks, 'ControllerProxy', FakeControllerProxy)
    tasks.setpilotwire()
    record = caplog.records[0]
    assert record.levelname == level
    assert record.message == message
