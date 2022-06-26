'''
TODO: document "docushare" module.
'''


from .docushare import DocuShare
from .handle import handle, Handle, HandleType, InvalidHandleError
from .parser import ParseError, parse_login_page, parse_property_page, parse_history_page
from .util import join_url

__all__ = [
    'DocuShare',

    'handle',
    'Handle',
    'HandleType',
    'InvalidHandleError',

    'ParseError',
    'parse_login_page',
    'parse_property_page',
    'parse_history_page',
    
    'join_url',
]

