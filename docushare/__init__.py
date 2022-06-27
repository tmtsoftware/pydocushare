'''
TODO: document "docushare" module.
'''


from .docushare import DocuShare, Resource, PasswordOption, DocuShareSystemError, DocuShareNotFoundError, DocuShareNotAuthorizedError
from .dsobject import DocuShareBaseObject, FileObject, DocumentObject, VersionObject
from .handle import handle, Handle, HandleType, InvalidHandleError
from .parser import ParseError, is_not_found_page, is_not_authorized_page, parse_if_system_error_page, parse_login_page, parse_property_page, parse_history_page
from .util import join_url

__all__ = [
    'DocuShare',
    'Resource',
    'PasswordOption',
    'DocuShareSystemError',
    'DocuShareNotFoundError',
    'DocuShareNotAuthorizedError',

    'DocuShareBaseObject',
    'FileObject',
    'DocumentObject',
    'VersionObject',

    'handle',
    'Handle',
    'HandleType',
    'InvalidHandleError',

    'ParseError',
    'is_not_found_page',
    'is_not_authorized_page',
    'parse_if_system_error_page',
    'parse_login_page',
    'parse_property_page',
    'parse_history_page',
    
    'join_url',
]

