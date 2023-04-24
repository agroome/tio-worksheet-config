from pydantic import BaseModel, Extra


class CustomBase(BaseModel, extra=Extra.allow):
    @property
    def describe(self):
        return f"creating: {repr(self)}"

    