
from pydantic import Extra, Field, validator
from typing import Optional
from models.base_model import CustomBase
from session import bind_api

@bind_api('networks')
class Network(CustomBase, extra=Extra.allow):
    name: str = Field(alias='network_name')
    description: Optional[str]
    assets_ttl_days: Optional[int] 

    @validator('assets_ttl_days')
    def validate_ttl(cls, value):
        if isinstance(value, int) and not 0 <= value <= 365:
            raise ValueError(f'[{value}]: assets_ttl_days must be between 90 and 365')
        return value
        

    def execute(self, tio):
        network = tio.networks.create(**self.dict())
        return network
