
import click
import workbook

@click.group()
def cli():
    '''entry point for CLI'''

@cli.command()
@click.argument('sheet_name')
@click.argument('filename', type=click.Path(exists=True))
def load(filename, sheet_name):
    '''load a single sheet from an excel file'''
    click.echo(f"loading {sheet_name} from {filename}")
    sheets = workbook.WorkSheets(filename)
    try:
        sheets.execute(sheet_name)
    except workbook.SheetNotFound as e:
        print(repr(e))


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def load_all(filename):
    '''load all sheets from excel file'''
    sheets = workbook.Worksheets(filename)
    for sheet_name in sheets.work_sheets:
        try:
            sheets.execute(sheet_name)
        except workbook.SheetNotFound as e:
            print(repr(e))

if __name__ == '__main__':
    cli()