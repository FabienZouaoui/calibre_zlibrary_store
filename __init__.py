__license__ = 'GPL 3'
__copyright__ = '2020, Fabien Zouaoui <fabien@zouaoui.org>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class ZLibraryStore(StoreBase):
    name = 'The Zlibrary Library'
    description = "Z-Library. The world's largest ebook library."
    author = 'Fabien Zouaoui'
    version = (0, 0, 10)
    drm_free_only = True
    #formats = ['EPUB', 'PDF', 'DJVU', 'FB2', 'TXT', 'RAR', 'MOBI', 'LIT', 'DOC', 'RTF']
    formats = ['EPUB']
    actual_plugin = 'calibre_plugins.store_zlibrary.zlibrary_plugin:ZLibraryStore'
