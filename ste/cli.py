#!/usr/bin/env python3

import click

from ste import decrypt as _decrypt
from ste import encrypt as _encrypt
from ste.client import client as _client
from ste.server import app


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        ctx.invoke(client)


@cli.command(short_help='Encrypt text by key')
@click.argument('plaintext')
@click.option('--key', '-k', default='', help='Key')
def encrypt(key, plaintext):
    click.echo(_encrypt(key, plaintext))


@cli.command(short_help='Decrypt text by key')
@click.argument('ciphertext')
@click.option('--key', '-k', default='', help='Key')
def decrypt(key, ciphertext):
    click.echo(_decrypt(key, ciphertext))


@cli.command(short_help='Run Client')
def client():
    _client()


@cli.command(short_help='Run as Web Server')
@click.option('--host', '-h', default='localhost', help='Listening Host')
@click.option('--port', '-p', default=80, help='Listening Port')
@click.option('--debug', is_flag=True)
def run(host, port, debug):
    app.run(host=host, port=port, debug=debug)


def main():
    cli()


if __name__ == '__main__':
    main()
