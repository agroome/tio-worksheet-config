from models.base_model import CustomBase
from typing import Optional
from datetime import datetime

class Exclusion(CustomBase):
    exclusion_name: str 
    exclusion_ipv4: str 
    enabled: Optional[bool]
    frequency: Optional[str]
    day_of_month: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    def execute(self, tio):
        try:    
            tio.exclusions.create(
                name=self.exclusion_name, 
                members=[self.exclusion_ipv4], 
                enabled=self.enabled,
                start_time=self.start_time, 
                end_time=self.end_time)
        except Exception as Argument:                                           
            print('error: ', str(Argument))    
