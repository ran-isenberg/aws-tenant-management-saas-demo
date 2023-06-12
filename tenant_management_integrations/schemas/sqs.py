from enum import Enum
from typing import Annotated, List, Optional, Union

from aws_lambda_powertools.utilities.parser.models import SqsModel, SqsRecordModel
from pydantic import BaseModel, Field, conlist

from tenant_management_integrations.schemas.sns import ActivateReq, CreateReq, DeleteReq, SuspendReq, UpdateReq


class ErrorType(str, Enum):
    GENERAL = 'GENERAL'
    RETRY = 'RETRY'


class ServiceError(BaseModel):
    message: str
    error_type: ErrorType


class Ack(BaseModel):
    request_id: str
    tenant_id: str
    service: str


class ServiceFailure(BaseModel):
    message: Annotated[str, Field(min_length=1)]
    category: Annotated[str, Field(min_length=1)]
    component: Annotated[str, Field(min_length=1)]
    error_type: ErrorType


# this schema is the basic response schema that each service pushes to the tenant mgmt fifo SQS
class ServiceResponse(Ack):
    failures: Optional[conlist(ServiceFailure, min_items=1)]
    endpoint: Optional[str]  # UI endpoint of the tenant
    api_endpoint: Optional[str]  # API endpoint of the tenant


class HardenedSqsRecordModel(SqsRecordModel):
    body: Union[CreateReq, UpdateReq, ActivateReq, DeleteReq, SuspendReq]


class HardenedSqsModel(SqsModel):
    Records: List[HardenedSqsRecordModel]
