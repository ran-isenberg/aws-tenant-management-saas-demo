# pylint: disable=no-name-in-module, no-self-argument,invalid-name
from enum import Enum


class EventType(str, Enum):
    ACTIVATE = 'activate'
    SUSPEND = 'suspend'
    DELETE = 'delete'
    UPDATE = 'update'
    NONE = ''


class ServicesEventType(str, Enum):
    CREATE = 'create'
    ACTIVATE = 'activate'
    SUSPEND = 'suspend'
    DELETE = 'delete'
    UPDATE = 'update'


class TenantMgmtException(Exception):
    pass
