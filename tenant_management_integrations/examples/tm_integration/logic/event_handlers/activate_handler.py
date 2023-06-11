from aws_lambda_powertools import Logger

from tenant_management_integrations.schemas.sns import ActivateReq


def handle_activate_event(activate_req: ActivateReq) -> None:
    logger = Logger()
    logger.info('starting to handle activate event')
