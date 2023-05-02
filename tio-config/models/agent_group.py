from models.base_model import CustomBase
from pydantic import Field, Extra
from tenable.io import TenableIO

from session import bind_api

@bind_api('agent_groups')
class AgentGroup(CustomBase):
    name: str = Field(alias='group_name')

    @property
    def describe(self):
        return f"AgentGroup(name='{self.name}')"

    def execute(self, tio: TenableIO):
        try:
            tio.agent_groups.create(self.name)
        except Exception as e:
            pass
            # print(f'warning: {e.args}')