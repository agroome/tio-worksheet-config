from pydantic import Extra, Field, validator
from typing import Optional
from models.base_model import CustomBase

class ScannerRoute(CustomBase):
    routes: list

class ScannerGroup(CustomBase):
    name: str 
    description: Optional[str]
    group_type: Optional[str] = Field(regex='load_balancing')
    assets_ttl_days: Optional[int] 

    def execute(self, tio):
        network = tio.scanner_groups.create(**self.dict())
        return network
