from aws_lambda_powertools import Logger

from tenant_management_integrations.schemas.sns import UpdateReq


def handle_update_event(update_req: UpdateReq) -> None:
    logger = Logger()
    logger.info('starting to handle update event')
