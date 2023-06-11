# aws-tenant-management-saas-demo

[![license](https://img.shields.io/github/license/ran-isenberg/aws-tenant-management-saas-demo)](https://github.com/ran-isenberg/aws-tenant-management-saas-demo/blob/master/LICENSE)
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.10&color=blue?style=flat-square&logo=python)
![version](https://img.shields.io/github/v/release/ran-isenberg/aws-tenant-management-saas-demo)
![github-star-badge](https://img.shields.io/github/stars/ran-isenberg/aws-tenant-management-saas-demo.svg?style=social)
![issues](https://img.shields.io/github/issues/ran-isenberg/aws-tenant-management-saas-demo)

![alt text](https://github.com/ran-isenberg/aws-tenant-management-saas-demo/blob/main/architecture.png?raw=true)

This repository contains code snippets and examples of an AWS Lambda handler function that implements tenant management requests sent via Amazon SNS & SQS.

There are three main function that represent a tenant management SDK that help service to integrate with the tenant management service (tm_sdk.py):
1. parse_tenant_mgmt_requests - parse input of SQS batch messages according to the tenant management service schemas
2. verify_tenant_mgmt_request - conduct security checks and verifications
3. send_response_to_tenant_mgmt_sqs - reply with success or failure to the tenant management SQS

In the architecture diagram, this is a sample implementation of 'Service x' or Service y', which triggers the tenant provisioning on their end.

This naive implementation assumes tenant creation takes less than 15 minutes (maximum time of a lambda).

For advanced use cases, you can use a step function state machine to handle the service tenant provision.

Further reading and general architecture: [SaaS factory demo of Tenant management service SDK and usage](https://aws.amazon.com/blogs/apn/how-cyberark-built-tenant-management-service-for-its-saas-offering/)
