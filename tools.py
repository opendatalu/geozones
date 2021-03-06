from contextlib import contextmanager
from os.path import basename
from urllib.request import urlopen, Request

import click


def _secho(template=None, **skwargs):
    def func(text, *args, **kwargs):
        text = text.format(*args, **kwargs)
        if template:
            text = template.format(text)
        click.secho(text, **skwargs)
    return func


title = _secho('>> {0}', fg='cyan', bold=True)
section = _secho('> {0}', bold=True)
info = _secho()
success = _secho(fg='green')
error = _secho(fg='red', bold=True)
warning = _secho(fg='yellow')


@contextmanager
def ok(text):
    try:
        click.secho('{0} ...... '.format(text), nl=False)
        yield
    except:
        error('ko')
        raise
    else:
        success('ok')


def unicodify(string):
    '''Ensure a string is unicode and serializable'''
    return string.decode('unicode_escape') if isinstance(string, bytes) else string


def extract_meta_from_headers(url):
    """Given a `url`, perform a HEAD request and return metadata."""
    req = Request(url, method='HEAD')
    req.add_header('Accept-Encoding', 'identity')
    response = urlopen(req)
    content_disposition = response.headers.get('Content-Disposition', '')
    if 'filename' in content_disposition:
        # Retrieve the filename and remove the last ".
        filename = content_disposition.split('filename="')[-1][:-1]
    else:
        filename = basename(url).strip()

    content_length = response.headers.get('Content-Length')
    if content_length:
        size = int(content_length)
    else:
        size = 1  # Fake for progress bar.

    return filename, size
