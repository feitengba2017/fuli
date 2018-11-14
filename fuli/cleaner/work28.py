import re
import scrapy
from w3lib.html import remove_tags
from .base_extractor import BaseExtractor
from .utils import SCRIPT_PLACEHOLDER, IMG_PLACEHOLDER, VIDEO_PLACEHOLDER


class Work28Extractor(BaseExtractor):

    def __init__(self):
        self.skip_css = '#ad'

    def parse_article_content(self, resp):
        contents = []
        scripts = []
        images, icount = [], 1
        videos, vcount = [], 1
        embeds, ecount = [], 1
        nodes = []

        nodes.extend(resp.css('.photo__ratio-enforced').xpath('node()').extract())
        nodes.extend(resp.css('.media-gallery__slider').xpath('node()').extract())
        nodes.extend(resp.css('.article-body>.text').xpath('node()').extract())

        for elem in nodes:
            sel = scrapy.Selector(text=elem, type='html')
            if sel.css(self.skip_css):
                continue
            elif sel.css('img'):
                icount = self.parse_image(
                    selector=sel,
                    src='img',
                    src_attr='@data-custom-lazy-loader|@src|@data-lazy-loader',
                    content=contents,
                    resource=images,
                    count=icount)
            elif sel.css('blockquote'):
                ecount = self.parse_embedded_html(
                    elem, contents, embeds, scripts, ecount)
            elif sel.css('iframe'):
                vcount = self.parse_video(
                    selector=sel,
                    src='iframe',
                    content=contents,
                    resource=videos,
                    count=vcount)
            elif sel.css('H1,H2,H3,H4,H5,ul,ol,li'):
                contents.append(remove_tags(elem, which_ones=('a',)))

            elif sel.css('p,div'):
                self.parse_paragraph(sel, contents)

        if scripts:
            contents.append(SCRIPT_PLACEHOLDER)
        return {'content': contents, 'image': images, 'video': videos,
                'embed': embeds, 'script': scripts}
