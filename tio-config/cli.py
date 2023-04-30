
import click
import click_pathlib
import pathlib

import workbook
import session

from tenable.io import TenableIO
from dotenv import load_dotenv
from pprint import pprint

DEFAULT_CONFIG = './tio-config.xlsx'
DEFAULT_ENV = './.env'

load_dotenv()
tio = TenableIO()
session.init(tio)

@click.group()
def cli():
    '''Configure Tenable.io instance based on worksheet data'''

@cli.command()
@click.argument('sheet_name')
@click.option('-c', '--config', type=click_pathlib.Path(exists=True), default=DEFAULT_CONFIG)
def load(sheet_name, config):
    '''load a single sheet from an excel file'''

    click.echo(f"loading {sheet_name} from {config}")
    ws = workbook.WorkSheets(config)
    
    try:
        objs = ws.get_objs('users', 'create')
    except workbook.SheetNotFound as e:
        print(repr(e))


@cli.command()
@click.option('-c', '--config', type=click_pathlib.Path(exists=True), default=DEFAULT_CONFIG)
def load_all(config):
    '''load all sheets from excel file'''

    sheets = workbook.Worksheets(config)
    for sheet_name in sheets.work_sheets:
        try:
            sheets.execute(sheet_name)
        except workbook.SheetNotFound as e:
            print(repr(e))


@cli.command()
@click.option('-k', '--keyfile', type=click_pathlib.Path(), default=DEFAULT_ENV)
def keys(keyfile: pathlib.Path):
    '''update environment file with Tenable.io keys'''

    if not keyfile.exists() or click.confirm('Overwrite existing file?'):
        access_key = click.prompt('Tenable.io access_key')
        secret_key = click.prompt('Tenable.io secret_key')
        click.echo(f'writing keys to {keyfile}...')
        with open(keyfile, 'w') as f:
            f.write(f'TIO_ACCESS_KEY={access_key}\nTIO_SECRET_KEY={secret_key}')
    else:
        click.echo('operation canceled...')


@cli.command()
# @click.argument('resource')
# @click.option('-f', '--fmt', type=str, help='python format string for output')
def tag_filters():
    '''dump asset tag filter names and supported operators'''
    
    records = tio.filters.asset_tag_filters()
    pprint(records)
    
    
def test_workbook(sheet, filename='tio-config.xlsx'):
    wb = workbook.WorkSheets(filename)
    records = wb.get_records(sheet)
    for record in records:
        print(record)


if __name__ == '__main__':
    from session import init_session
    init_session(tio)
    test_workbook('tags_ipv4')
    test_workbook('users')

    # wb = workbook.WorkSheets('tio-config.xlsx')
    # print(wb.get_records('users'))
    # cli()

