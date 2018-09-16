import datetime

from toggl.api import base
from toggl import exceptions
import pytest


#########################################################################################
# PropertyField

class PropertyFieldStore:
    value = None


def getter(name, instance, serializing=False):
    assert name == 'field'

    return PropertyFieldStore.value


def setter(name, instance, value, init=False):
    PropertyFieldStore.value = value


class PropertyEntity(base.TogglEntity):
        field = base.PropertyField(getter, setter)


class ReadOnlyPropertyEntity(base.TogglEntity):
        field = base.PropertyField(base.PropertyField.default_getter)


class TestPropertyField:

    def test_init(self):
        PropertyFieldStore.value = None
        PropertyEntity()
        assert PropertyFieldStore.value is None

        PropertyFieldStore.value = None
        PropertyEntity(field='some value')
        assert PropertyFieldStore.value == 'some value'

    def test_set_and_get(self):
        PropertyFieldStore.value = None
        instance = PropertyEntity()

        instance.field = 'some value'
        assert PropertyFieldStore.value == 'some value'
        assert instance.field == 'some value'

    def test_deserialization(self):
        PropertyFieldStore.value = None
        instance = PropertyEntity.deserialize()

        assert PropertyFieldStore.value is None
        assert instance.field is None

        PropertyFieldStore.value = None
        instance = PropertyEntity.deserialize(field='some value')

        assert PropertyFieldStore.value == 'some value'
        assert instance.field == 'some value'

    def test_read_only(self):
        PropertyFieldStore.value = None
        instance = ReadOnlyPropertyEntity()

        with pytest.raises(exceptions.TogglException):
            instance.field = 'some value'

        PropertyFieldStore.value = None
        instance = ReadOnlyPropertyEntity(field='some value')
        assert instance.field == 'some value'
        assert instance.__fields__['field'].is_read_only == True
        with pytest.raises(exceptions.TogglException):
            instance.field = 'some value'


#########################################################################################
# DateTimeField

class DateTimeEntity(base.TogglEntity):
    field = base.DateTimeField()


class TestDateTimeField:

    def test_type_check(self):
        instance = DateTimeEntity()

        with pytest.raises(TypeError):
            instance.field = 'some value not datetime'

        try:
            instance.field = datetime.datetime.now()
        except TypeError:
            pytest.fail('DateTimeField does not accept valid datetime object!')
