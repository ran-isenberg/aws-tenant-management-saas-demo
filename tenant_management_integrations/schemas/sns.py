from typing import List, Literal

from pydantic import BaseModel

from tenant_management_integrations.schemas.common import ServicesEventType


# this is the request tenant mgmt publishes to SNS to the services
class ServiceReq(BaseModel):
    name: str
    request_id: str
    tenant_id: str
    event_type: ServicesEventType
    services: List[str]
    region: str
    tenant_type: Literal['PRODUCTION', 'POC', 'TESTING']


class CreateReq(ServiceReq):
    pass


class SuspendReq(ServiceReq):
    pass


class DeleteReq(ServiceReq):
    pass


class ActivateReq(ServiceReq):
    pass


class UpdateReq(ServiceReq):
    pass
