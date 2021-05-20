# -*- coding: utf-8 -*-

author_info = (
    ('Ruslan Popov', 'ruslan.popov@gmail.com'),
)

package_license = 'HALFAKOP'
package_info = 'Demo Telegram Bot'

__VERSION__ = '0.1.0'
__version__ = __VERSION__.split('.')
__author__ = ', '.join('{} <{}>'.format(*author) for author in author_info)

__all__ = (
    __author__,
    __version__,
    package_info,
    package_license,
)
