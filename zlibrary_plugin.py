#!/usr/bin/python3
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2020, Fabien Zouaoui <fabien@zouaoui.org>

store_version = 15  # Needed for dynamic plugin loading

import urllib3
from urllib.parse import quote
from contextlib import closing

from lxml import html

from PyQt5.Qt import QUrl

from calibre import browser, url_slash_cleaner
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
ROOT = 'https://de1lib.org/'

class ZLibraryStore(BasicStoreConfig, StorePlugin):

    def open(self, parent=None, detail_item=None, external=False):
        url = ROOT

        if external or self.config.get('open_external', False):
            open_url(QUrl(url_slash_cleaner(detail_item if detail_item else url)))
        else:
            d = WebStoreDialog(self.gui, url, parent, detail_item)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get('tags', ''))
            d.exec_()

    def search(self, query, max_results=10, timeout=60):
        url  = ROOT + '/s/' + quote(query)

        br = browser(user_agent=USER_AGENT)

        counter = max_results
        with closing(br.open(url, timeout=timeout)) as f:
            doc = html.fromstring(f.read())

            for data in doc.xpath('//div[@id="searchResultBox"]/div'):
                if counter <= 0:
                    break

                # When I'm using xpath directly on data, the entire tree is parsed instead of the node.
                sub = html.fromstring(html.tostring(data))

                cover_url = ''.join(sub.xpath('//img[@class="cover lazy"]/@data-src'))
                if not cover_url:
                    cover_url = ROOT + ''.join(sub.xpath('//img[@class="cover"]/@src'))

                title       = ''.join(sub.xpath('//h3/a/text()'))
                author      = ', '.join(sub.xpath('//div[@class="authors"]/a/text()'))
                detail_item = ROOT + ''.join(sub.xpath('//h3[@itemprop="name"]/a/@href'))

                counter -= 1

                s = SearchResult()
                s.cover_url   = cover_url.strip()
                s.title       = title.strip()
                s.author      = author.strip()
                s.price       = '$0.00'
                s.detail_item = detail_item.strip()
                s.drm         = SearchResult.DRM_UNLOCKED
                s.formats = 'EPUB'
                #s.downloads['EPUB'] = data['url'].strip() + '.epub'

                yield s
