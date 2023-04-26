
import click
import click_pathlib
import pathlib
import workbook

from tenable.io import TenableIO
from dotenv import load_dotenv
from pprint import pprint

DEFAULT_CONFIG = './tio-config.xlsx'
DEFAULT_ENV = './.env'

load_dotenv()
tio: TenableIO = TenableIO()

@click.group()
def cli():
    '''Configure Tenable.io instance based on worksheet data'''

@cli.command()
@click.argument('sheet_name')
@click.option('-c', '--config', type=click_pathlib.Path(exists=True), default=DEFAULT_CONFIG)
def load(sheet_name, config):
    '''load a single sheet from an excel file'''

    click.echo(f"loading {sheet_name} from {config}")
    sheets = workbook.WorkSheets(config)
    try:
        sheets.execute(sheet_name)
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
@click.argument('resource')
@click.option('-f', '--fmt', type=str, help='python format string for output')
def filters(resource, fmt):
    click.echo(f'listing {resource} fmt="{fmt}"')
    try:
        api_method = getattr(tio.filters, resource)
        print(f'api: {api_method}')
    except TypeError:
        click.BadParameter(f'[tio.filters.{resource}]: pyTenable api binding not found')
    records = api_method()
    pprint(records)

    
    
if __name__ == '__main__':
    cli()