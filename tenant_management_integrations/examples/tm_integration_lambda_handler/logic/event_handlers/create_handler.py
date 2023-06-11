from aws_lambda_powertools import Logger

from tenant_management_integrations.schemas.sns import CreateReq


def handle_create_event(create_req: CreateReq) -> None:
    logger = Logger()
    logger.info('starting to handle create event')
