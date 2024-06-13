import os
from typing import Dict

from pydantic import BaseModel, Field


class SubServiceDefinition(BaseModel):
    title: str = Field(..., description='The title of the sub-service', examples=['Digital Twin'])
    emoji: str = Field(..., description='An emoji representing the sub-service', examples=['🤖'])
    description: str = Field(..., description='A short description of the sub-service',
                             examples=['Manage your digital twin'])


class ServiceDefinition(BaseModel):
    title: str = Field(..., description='The title of the cloud service', examples=['Virtual Machines'])
    emoji: str = Field(..., description='An emoji representing the cloud service', examples=['💻'])
    description: str = Field(..., description='A short description of the cloud service',
                             examples=['Create and manage virtual machines'])
    sub_services: Dict[str, SubServiceDefinition] = Field(...,
                                                          description='The sub-services of the cloud service')


class ServiceDefinitions(BaseModel):
    services: Dict[str, ServiceDefinition] = Field(...,
                                                   description='The cloud services provided by the cloud provider')


services = ServiceDefinitions.parse_file(os.path.join(os.path.dirname(__file__), 'services.json')).services
