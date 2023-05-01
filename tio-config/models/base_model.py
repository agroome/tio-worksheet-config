import re

from pydantic import BaseModel, Extra, root_validator
from typing import Any, Dict


class CustomBase(BaseModel, extra=Extra.allow, anystr_strip_whitespace=True):

    @root_validator(pre=True)
    def build_filters(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        def strip_lines(value):
            # replace newlines and remove spaces around commas
            if isinstance(value, str):
                value = re.sub('\n+', ',', value.strip())
                value = re.sub('[ ]*,[ ]*', ',', value)
            return value

        return {strip_lines(k): strip_lines(v) for k, v in values.items()}
         

    @property
    def describe(self):
        return f"creating: {repr(self)}"

    