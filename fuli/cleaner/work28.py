import scrapy
from w3lib.html import remove_tags
from .base_extractor import BaseExtractor
from .utils import SCRIPT_PLACEHOLDER
from fuli.newitem import NewsItem


class Work28Extractor(BaseExtractor):

    def __init__(self):
        self.skip_css = '#ad,.shareBox,#cambrian0'

    def parse_article_content(self, resp):
        contents = []
        scripts = []
        images, icount = [], 1
        videos, vcount = [], 1
        embeds, ecount = [], 1
        nodes = []

        nodes.extend(resp.css('.article_content').xpath('node()').extract())

        for elem in nodes:
            sel = scrapy.Selector(text=elem, type='html')
            if sel.css(self.skip_css):
                continue
            elif sel.css('img'):
                icount = self.parse_image(
                    selector=sel,
                    src='img',
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

    def process_item(self, resp):
        item = NewsItem()
        res = self.parse_article_content(resp)
        item['content'] = res['content']
        item['img_src'] = res.get('image', [])
        item['video_src'] = res['video']
        item['embed_html'] = res.get('embed', [])
        item['script_src'] = list(set(res.get('script', [])))
        return item
