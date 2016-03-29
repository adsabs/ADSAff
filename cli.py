import click
import importer

DEBUG = False

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    if debug:
        click.echo('Debug mode is on')
        global DEBUG
        DEBUG = True

    
            
@cli.command()
@click.argument('fprefix')
def info(fprefix):
    affs = importer.load_affiliations(fprefix)
    print 'Total numbef of objects:', len(affs)
    print 'Affiliations with parents', len(filter(lambda x: x.parent, affs.values()))
    
    total_len = 0
    total_names = 0
    total_words = 0
    for a in affs.values():
        total_len += sum(map(lambda x: len(x), a.other_names)) + len(a.value)
        total_names += len(a.other_names) + 1
        total_words += sum(map(lambda x: len(x.split(' ')), a.other_names)) + len(a.value.split(' '))
        
    print 'Average length of names:', total_len / total_names
    print 'Average number of names:', total_names / len(affs)
    print 'Average number of words per aff:', total_words / total_names


if __name__ == '__main__':
    cli()
