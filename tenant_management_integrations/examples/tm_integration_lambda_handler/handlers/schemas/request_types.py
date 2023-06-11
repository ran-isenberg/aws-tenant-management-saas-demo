from typing import TypeVar, Union

from tenant_management_integrations.schemas.sns import ActivateReq, CreateReq, DeleteReq, SuspendReq, UpdateReq

RequestModel = TypeVar('RequestModel', bound=Union[CreateReq, UpdateReq, ActivateReq, DeleteReq, SuspendReq])
