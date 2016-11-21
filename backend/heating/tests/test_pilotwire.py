# -*- coding: utf-8 -*-

from collections import namedtuple

import pytest
from pilotwire_controller.client import PilotwireModesInconsistent

from .. import tasks


STATUS_MSG = [
    "Pilotwire controller status changed from {} to {}",
    ", going to set pilotwire modes"
]


class FakeControllerProxy:

    TEST_TYPE = 'undefined'

    def __init__(self, _):
        self.count = 0

    def check_status(self):
        if self.TEST_TYPE.startswith('status_'):
            return self.TEST_TYPE[7:]

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
    ('modes_inconsistent', 'ERROR', "Inconsistent test"),
])
@pytest.mark.django_db
def test_set_modes(monkeypatch, caplog, test_type, level, message):
    FakeControllerProxy.TEST_TYPE = test_type
    monkeypatch.setattr(tasks.pilotwire, 'ControllerProxy',
                        FakeControllerProxy)
    tasks.pilotwire.set_modes()
    record = caplog.records[0]
    assert record.levelname == level
    assert record.message == message


def test_is_active(patched_redis):
    assert not tasks.pilotwire.is_active()
    patched_redis.set(tasks.pilotwire.REDIS_KEY, 'undefined')
    assert not tasks.pilotwire.is_active()
    patched_redis.set(tasks.pilotwire.REDIS_KEY, 'active')
    assert tasks.pilotwire.is_active()


Params = namedtuple('Params', [
    'keyval', 'test_type', 'exp_msg'
])


@pytest.mark.parametrize('params', [
    Params(None, 'status_active', STATUS_MSG[0] + STATUS_MSG[1]),
    Params('active', 'status_error', STATUS_MSG[0]),
    Params('undefined', 'status_undefined', None),
], ids=["None to active", "active to error", "undefined to undefined"])
@pytest.mark.django_db
def test_update_status(caplog, monkeypatch, patched_redis, params, mailoutbox):
    new_status = params.test_type[7:]
    FakeControllerProxy.TEST_TYPE = params.test_type
    monkeypatch.setattr(tasks.pilotwire, 'ControllerProxy',
                        FakeControllerProxy)
    patched_redis.set(tasks.pilotwire.REDIS_KEY, params.keyval,
                      xx=True if params.keyval is None else False)
    tasks.pilotwire.update_status()
    assert patched_redis.get(tasks.pilotwire.REDIS_KEY) == new_status.encode()
    assert 0 < patched_redis.ttl(tasks.pilotwire.REDIS_KEY) <= 90
    log_filtered = [r for r in caplog.records if r.name == 'heating.pilotwire']
    if params.exp_msg:
        expected = params.exp_msg.format(params.keyval, new_status)
        assert log_filtered[0].levelname == (
            'INFO' if params.test_type == 'status_active' else 'ERROR')
        assert log_filtered[0].message == expected
        if params.test_type != 'status_active':
            assert mailoutbox[0].subject == (
                "[Django] Pilotwire controller connection error")
            assert expected in mailoutbox[0].body
    else:
        assert log_filtered == []
