from aws_lambda_powertools import Logger

from tenant_management_integrations.schemas.sns import DeleteReq


def handle_delete_event(delete_req: DeleteReq) -> None:
    logger = Logger()
    logger.info('starting to handle delete event')
