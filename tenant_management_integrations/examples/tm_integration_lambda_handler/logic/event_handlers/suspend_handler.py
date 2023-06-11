from aws_lambda_powertools import Logger

from tenant_management_integrations.schemas.sns import SuspendReq


def handle_suspend_event(suspend_req: SuspendReq) -> None:
    logger = Logger()
    logger.info('starting to handle suspend event')
