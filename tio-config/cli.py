
import click
import workbook

DEFAULT_CONFIG = './tio-config.xlsx'

@click.group()
def cli():
    '''entry point for CLI'''

@cli.command()
@click.argument('sheet_name')
@click.option('-c', '--config', type=click.Path(exists=True), default=DEFAULT_CONFIG)
def load(sheet_name, config):
    '''load a single sheet from an excel file'''
    click.echo(f"loading {sheet_name} from {config}")
    sheets = workbook.WorkSheets(config)
    try:
        sheets.execute(sheet_name)
    except workbook.SheetNotFound as e:
        print(repr(e))


@cli.command()
@click.option('-c', '--config', type=click.Path(exists=True), default=DEFAULT_CONFIG)
def load_all(config):
    '''load all sheets from excel file'''
    sheets = workbook.Worksheets(config)
    for sheet_name in sheets.work_sheets:
        try:
            sheets.execute(sheet_name)
        except workbook.SheetNotFound as e:
            print(repr(e))

if __name__ == '__main__':
    cli()