from typing import Union
from urllib import parse as urlparse

urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mqtt')
urlparse.uses_netloc.append('https')
urlparse.uses_netloc.append('http')


def decompose(value: str) -> dict:
    url = urlparse.urlparse(value)
    name = url.path[1:]
    return {
        'scheme': url.scheme,
        'username': url.username,
        'password': url.password,
        'hostname': url.hostname,
        'port': url.port,
        'name': None if len(name) == 0 else name,
        }


def compose(hostname: str,
            port: Union[str, int] = '',
            scheme: str = '',
            username: str = '',
            password: str = '',
            name: str = '') -> str:
    if scheme:
        scheme = f'{scheme}://'
    if username:
        if password:
            username = f'{username}:{password}@'
        else:
            username = f'{username}@'
    if port:
        port = f':{port}'
    if name:
        name = f'/{name}'
    return f'{scheme}{username}{hostname}{port}{name}'


def hide_string(value: str) -> str:
    """ Hide the center of the string."""
    if len(value) < 3:
        return value
    limit = len(value) // 3
    if limit > 4:
        limit = 4
    return value[:limit] + '*' * limit + value[-limit:]


def safe_url(value: str) -> str:
    """ Hide password from url string.

    For example:

    >>> safe_url('postgres://root:top_secret@localhost:5432/xkee')
    'postgres://root:top***ret@localhost:5432/xkee'
    >>> safe_url('postgres://localhost:5432/xkee')
    'postgres://localhost:5432/xkee'
    >>> safe_url('postgres://user@localhost:5432/xkee')
    'postgres://user@localhost:5432/xkee'
    >>> safe_url('')
    ''
    >>> safe_url(123)
    Traceback (most recent call last):
    ...
    TypeError: 'value' must be a string
    """
    if not isinstance(value, str):
        raise TypeError('\'value\' must be a string')
    prs = urlparse.urlparse(value)
    if all(prs._userinfo):
        _netloc = prs.netloc[prs.netloc.find('@') :]
        prs = prs._replace(
            netloc=f'{prs.username}:{hide_string(prs.password)}{_netloc}')
        return urlparse.urlunparse(prs)
    return value
