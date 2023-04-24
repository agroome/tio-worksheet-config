
import re
import textwrap

from base_model import CustomBase
from pydantic import Field, Extra, root_validator
from typing import Any, Dict, List, ClassVar
from tenable.io import TenableIO

tag_column_regex = re.compile('(?P<name>\w+)_(?P<operator>\w+)')


class InvalidTagColumn(Exception):
    '''tag item name must be in filters returned by tio.filters.asset_tags()'''


class InvalidTagFilter(Exception):
    '''tag item name must be in filters returned by tio.filters.asset_tags()'''


class Tag(CustomBase, extra=Extra.allow):
    category: str = Field(include=True, alias='tag_category')
    value: str = Field(include=True, alias='tag_value')
    filters: List = Field(include=True)
    filter_type: str = Field(include=True, default='and')
        
    @root_validator(pre=True)
    def build_filters(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        '''Build the filter statement based on "extra fields" in values'''

        def strip_lines(value):
            # remove outer whitespace and newlines
            value = re.sub('\n+', ',', value.strip())
            # remove spaces around commas
            return re.sub('[ ]*,[ ]*', ',', value)

        # identify required_fields so we can skip these in the loop below
        required_field_names = {field.alias for field in cls.__fields__.values() if field.alias != 'extra'}
                
        filters = []
        for field_name, field_value in values.items():
            if field_name not in required_field_names:
                # parse col header to identify filter_name and operator, i.e. ipv4_eq
                match = re.match('(?P<filter_name>\w+)_(?P<operator>\w+)', field_name.lower())
                if match is None:
                    raise InvalidTagColumn(f'[{field_name}]: expecting <filter_name>_<operator>')
    
                filter_name, operator = match.groups()                    
                field_value = strip_lines(field_value)
                filters.append((filter_name, operator, field_value))
                
        values['filters'] = filters
        return values

    @property
    def describe(self):
        filter_statements = '\n'.join([f'    {line}' for line in self.filters])
            
        text = f'''
        creating Tag(
            category="{self.category}"
            value="{self.value}"
            filter_type="{self.filter_type}")
            filters = [
                {filter_statements}
            ]
        )'''
        return textwrap.dedent(text)

    def execute(self, tio: TenableIO):
        try:
            tio.tags.create(**self.dict())
        except Exception as e:
            print(f'warning: {str(e)}')