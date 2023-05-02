from session import bind_api, get_cached
from models.base_model import CustomBase

@bind_api('groups')
class Group(CustomBase):
    name: str

    @property
    def id(self) -> int:
        groups = get_cached('groups')
        group = groups.get(self.name)
        return group['id']
