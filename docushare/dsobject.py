from abc import ABC
from pathlib import Path

from .handle import Handle, HandleType


class DocuShareBaseObject(ABC):
    '''Represents one object in DocuShare.

    Parameters
    ----------
    docushare : DocuShare
        The DocuShare site that this object belongs to.
    hdl : Handle
        The DocuShare handle that represents this object.
    '''
    
    def __init__(self, docushare, hdl):
        from .docushare import DocuShare
        if not isinstance(docushare, DocuShare):
            raise TypeError('docushare must be an instance of DocuShare')
        if not isinstance(hdl, Handle):
            raise TypeError('hdl must be an instance of Handle')
        
        self.__docushare = docushare
        self.__hdl       = hdl

    @property
    def docushare(self):
        '''DocuShare : The DocuShare site that this object belongs to.'''
        return self.__docushare

    @property
    def handle(self):
        '''Handle : The DocuShare handle that represents this object.'''
        return self.__hdl

    def __str__(self):
        return f'handle: "{self.handle}"'

class FileObject(DocuShareBaseObject):
    '''Represents one file object in DocuShare.

    Parameters
    ----------
    docushare : DocuShare
        The DocuShare site that this object belongs to.
    hdl : Handle
        The DocuShare handle that represents this object.
    title : str
        Title of this file.
    filename : str
        File name of this file.
    '''
    
    def __init__(self, docushare, hdl, title, filename):        
        super().__init__(docushare, hdl)
        
        if not isinstance(title, str):
            raise TypeError('title must be str')
        if not isinstance(filename, str):
            raise TypeError('filename must be str')

        self._title     = title
        self._filename  = filename
    
    @property
    def title(self):
        '''str : Title of this document.'''
        return self._title

    @property
    def filename(self):
        '''str : File name of this document.'''
        return self._filename

    def __str__(self):
        return f'handle: "{self.handle}", title: "{self.title}", filename: "{self.filename}"'
    
    @property
    def download_url(self):
        '''str : URL to download this document.'''
        from .docushare import Resource
        return self.docushare.url(Resource.Get, self.handle)

    def download(self, path = None, size_for_progress_report = 1000000):
        '''Download this document from the DocuShare site to the local storage.

        Parameters
        ----------
        path : path-like object or None
            If it is None, this method downloads the document as a file in the current directory
            and the file name is determined as suggested by the DocuShare site.
            If it is a directory path, the document is downloaded as a file in the given directory
            and the file name is determined as suggested by the DocuShare site.
            If the given path is not a directory or does not exist, the document is downloaded
            as a file to the given path.
        size_for_progress_report : int
            This method shows a progress bar using `tqdm <https://tqdm.github.io/>` if the file size is
            more than the specified size in bytes.

        Returns
        -------
        path-like object
            Path to the downloaded file.
        '''
        if path is None:
            path = Path.cwd()
        else:
            path = Path(path)
            
        if path.is_dir():
            path = path.joinpath(self.filename)
            
        self.docushare.download(self.handle, path, size_for_progress_report = size_for_progress_report)
        return path

class DocumentObject(FileObject):
    '''Represents one Document object in DocuShare.

    Parameters
    ----------
    docushare : DocuShare
        The DocuShare site that this object belongs to.
    hdl : Handle
        The DocuShare handle that represents this object. The type must be :py:enum:`HandleType.Document`.
    title : str
        Title of this document.
    filename : str
        File name of this document.
    document_control_number : str or None
        Document conrol number of this document. This can be None if document control number is not defined.
    version_handles : list
        Version handles of this document. :py:class:`list` of :py:class:`Handle` instances.'
    '''
    
    def __init__(self, docushare, hdl, title, filename, document_control_number, version_handles):
        super().__init__(docushare, hdl, title, filename)
        
        if hdl.type != HandleType.Document:
            raise ValueError('handle type must be Document')
        if not isinstance(document_control_number, (str, type(None))):
            raise TypeError('document_control_number must be str or None')
        if not isinstance(version_handles, list):
            raise TypeError('verion_handles must be list')
        if not all([isinstance(version_handle, Handle) for version_handle in version_handles]):
            raise TypeError('All elements in verion_handles must be instances of Handle')
        if not all([hdl.type == HandleType.Version for hdl in version_handles]):
            raise TypeError('All handle types in verion_handles must be Version')
        
        self._document_control_number = document_control_number
        self._version_handles         = version_handles

    @property
    def document_control_number(self):
        '''str : Document control number.'''
        return self._document_control_number

    def __str__(self):
        return f'handle: "{self.handle}", title: "{self.title}", filename: "{self.filename}", document_control_number: "{self.document_control_number}"'

    @property
    def version_handles(self):
        ''':py:class:`list` of :py:class:`Handle`: Version handles of this document.'''
        return self._version_handles

    @property
    def versions(self):
        ''':py:class:`list` of :py:class:`VersionObject`: Version objects of this document.'''
        return [self.docushare[ver_hdl] for ver_hdl in self.version_handles]

class VersionObject(FileObject):
    '''Represents one Version object in DocuShare.

    Parameters
    ----------
    docushare : DocuShare
        The DocuShare site that this object belongs to.
    hdl : Handle
        The DocuShare handle that represents this object. The type must be :py:enum:`HandleType.Version`.
    title : str
        Title of this version.
    filename : str
        File name of this version.
    version_number : int
        Version number of this version.
    '''
    
    def __init__(self, docushare, hdl, title, filename, version_number):
        super().__init__(docushare, hdl, title, filename)
        if hdl.type != HandleType.Version:
            raise ValueError('handle type must be Version')
        
        self._version_number = version_number

    @property
    def version_number(self):
        '''int : version number (a sequential number)'''
        return self._version_number

    def __str__(self):
        return f'handle: "{self.handle}", title: "{self.title}", filename: "{self.filename}", version_number: {self.version_number}'

class CollectionObject(DocuShareBaseObject):
    '''Represents one Collection object in DocuShare.

    Parameters
    ----------
    docushare : DocuShare
        The DocuShare site that this object belongs to.
    hdl : Handle
        The DocuShare handle that represents this object. The type must be :py:enum:`HandleType.Collection`.
    title : str
        Title of this collection.
    object_handles : list
        Handles of the objects under this collection. :py:class:`list` of :py:class:`Handle` instances.'
    '''
    
    def __init__(self, docushare, hdl, title, object_handles):
        super().__init__(docushare, hdl)
        
        if hdl.type != HandleType.Collection:
            raise ValueError('handle type must be Collection')
        if not isinstance(title, str):
            raise TypeError('title must be str')
        if not isinstance(object_handles, list):
            raise TypeError('object_handles must be list')
        if not all([isinstance(object_handle, Handle) for object_handle in object_handles]):
            raise TypeError('All elements in object_handles must be instances of Handle')
        
        self._title          = title
        self._object_handles = object_handles

    @property
    def title(self):
        '''str : Title of this collection.'''
        return self._title

    def __str__(self):
        return f'handle: "{self.handle}", title: "{self.title}"'

    @property
    def object_handles(self):
        ''':py:class:`list` of :py:class:`Handle`: Handles of the objects under this collection.'''
        return self._object_handles

