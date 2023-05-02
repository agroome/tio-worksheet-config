
import re
import textwrap

from pydantic import Field, Extra, root_validator
from typing import Any, Dict, List, ClassVar, Optional, Tuple
from tenable.io import TenableIO
from dotenv import load_dotenv

from session import bind_api, get_cached

from models.base_model import CustomBase
# from commands.cache import get_cached_tag_filters, get_cached_users


tag_column_regex = re.compile('(?P<name>\w+)_(?P<operator>\w+)')


class InvalidTagColumn(Exception):
    '''column name must be in filters list by tio.filters.asset_tags()'''


class InvalidTagFilter(Exception):
    '''tag item name must be in filters returned by tio.filters.asset_tags()'''


@bind_api('tags')
class Tag(CustomBase, extra=Extra.allow):
    category: str = Field(include=True, alias='tag_category')
    value: str = Field(include=True, alias='tag_value')
    filter_type: str = Field(include=True, default='and')
    filters: List = Field(include=True, default_factory=list)
        
    @root_validator(pre=True)
    def build_filters(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        '''Build the filter statement based on multiple columns.'''

        # fields defined in the class definition (or their alias)
        required_field_names = [field.alias for field in cls.__fields__.values()]
        # filter_values are all values execept required_field_names
        filter_values = {k: v for k, v in values.items() if k not in required_field_names}

        filters = []
        for field_name, field_value in filter_values.items():
            filter_name, operator = parse_filter_name(field_name)
            if field_value is None:
                continue

            field_value = re.sub('\n+', ',', field_value.strip())
            field_value = re.sub('[ ]*,[ ]*', ',', field_value)

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
def parse_filter_name(column_name: str) -> Tuple[dict, str]:
    '''split value into (filter_name, operator)
    
    The filter column headers will be either:
        - the name of a filter, i.e. ipv4
        - OR the <name><' ' or '_'><operator
    
    '''

    # default to equal when the value is a filter_name with out the operator
    operator = 'eq'
    filter_name = column_name
    
    # get the dictionary of valid filter names and operators
    tag_filters = get_cached('asset_tag_filters')
    tag_filter = tag_filters.get(column_name)

    if tag_filter is None:
        # see if there is an operator appended to the filter_name
        match = re.match('(?P<filter_name>\w+)[ _](?P<operator>\w+)', column_name)
        if match is None:
            raise ValueError(f'[{column_name}]: bad format')
            
        filter_name, operator = match.groups()
        tag_filter = tag_filters.get(filter_name)

        if tag_filter is None:
            raise KeyError(f'[{filter_name}]: filter name not found')
    
        if operator not in tag_filter['operators']:
            raise KeyError(f'[{operator}]: not in {tag_filter["operators"]}')

    return filter_name, operator
        
