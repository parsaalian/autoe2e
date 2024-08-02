import click

from oraclai.main import run


@click.command()
@click.option('--config', default=None, help='path to config file')
def main(config: str):
    run(config)


if __name__ == '__main__':
    main()
