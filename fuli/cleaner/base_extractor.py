from w3lib.html import remove_tags
import scrapy
from .utils import (PLACEHOLDER, INSTAGRAM_SCRIPT, TWITTER_SCRIPT,
                   IMGUR_SCRIPT, CLOUDFRONT_SCRIPT, GRAPHIQ_SCRIPT,
                   ADOBE_SPARK_SCRIPT, PINTEREST_SCRIPT, PLAYBUZZ_SCRIPT,
                   BRIGHTCOVE_SCRIPT, TWITTER_TIMELINE_SCRIPT, APESTER_SCRIPT,
                   CURALATE_SCRIPT, FLICKR_SCRIPT,
                   TUMBLR_SCRIPT, GFM_SCRIPT, CEROS_SCRIPT)


class BaseExtractor(object):

    def delete_tags(self, text):
        """Remove all tags"""
        return remove_tags(text)

    def parse_paragraph(self, selector, content_list, tag='p'):
        """
        arguemnts:
        selector: scrapy.Selector.
        content_list: article content list.
        tag: paragraph tag.
        """
        text = ''.join(selector.css(tag).xpath(
            'node()').extract()).strip()
        if text:
            text = remove_tags(
                text, which_ones=('a', 'meta', 'script', 'span'))
            content_list.append(text)

    def is_ignore_styles(self, resp, styles):
        """If response has styles tags"""
        for style in styles:
            if resp.css(style):
                return True
        return False

    def parse_embedded_html(self, elem, content, resource, scripts, count):
        selector = scrapy.Selector(text=elem, type='html')
        script = ''
        ref = PLACEHOLDER['embedded_html'].format(count)
        count += 1
        res = {'html': elem, 'ref': ref}
        content.append(ref)
        resource.append(res)
        if (selector.css('.instagram-media') or
                'instagram.com' in elem):
            script = INSTAGRAM_SCRIPT
        elif (selector.css('.twitter-tweet')or
                selector.css('.twitter-video') or
                selector.css('.js-tweet')):
            script = TWITTER_SCRIPT
        elif selector.css('.twitter-timeline'):
            script = TWITTER_TIMELINE_SCRIPT
        elif selector.css('.imgur-embed-pub'):
            script = IMGUR_SCRIPT
        elif selector.css('.ftb-widget'):
            script = GRAPHIQ_SCRIPT
        elif selector.css('.asp-embed-link'):
            script = ADOBE_SPARK_SCRIPT
        elif selector.css('a ::attr(data-pin-do)'):
            script = PINTEREST_SCRIPT
        elif selector.css('.pb_feed'):
            script = PLAYBUZZ_SCRIPT
        elif selector.css('.BrightcoveExperience'):
            script = BRIGHTCOVE_SCRIPT
        elif selector.css('interaction'):
            script = APESTER_SCRIPT
        elif selector.css('.curalate-widget'):
            script = CURALATE_SCRIPT
        elif selector.css('.gfm-media-widget'):
            script = GFM_SCRIPT
        elif selector.css('a'):
            script = CLOUDFRONT_SCRIPT
        elif selector.css('.tumblr-post'):
            script = TUMBLR_SCRIPT
        elif selector.css('.ceros-experience'):
            script = CEROS_SCRIPT
        elif '//embedr.flickr.com' in elem:
            script = FLICKR_SCRIPT
        if script:
            scripts.append(script)
        return count

    def parse_image(self, **kwargs):
        '''
        arguemnts:
        selector: scrapy.Selector.
        src: image src css path.
        desc: description css path, if desc_path doesn't
                   exist, then description is a empty string.
        content: article content list.
        resource: article resource list.
        count: image counter.
        '''
        kwargs['type'] = 'image'
        return self.parse_resource(**kwargs)

    def parse_video(self, **kwargs):
        '''
        arguemnts:
        selector: scrapy.Selector.
        src: video src css path.
        src_attr: image src attribute, default is None, if src_attr is given,
                   then extract image url from this attribute instead of src.
        desc: description css path, if desc_path doesn't
                   exist, then description is a empty string.
        content: article content list.
        resource: article resource list.
        count: video counter.
        '''
        kwargs['type'] = 'video'
        return self.parse_resource(**kwargs)

    def parse_audio(self, **kwargs):
        '''
        arguemnts:
        selector: scrapy.Selector.
        src: audio src css path.
        src_attr: video src attribute, default is None, if src_attr is given,
                   then extract video url from this attribute instead of src.
        desc: description css path, if desc_path doesn't
                   exist, then description is a empty string.
        content: article content list.
        resource: article resource list.
        count: audio counter.
        '''
        kwargs['type'] = 'audio'
        return self.parse_resource(**kwargs)

    def parse_resource(self, **kwargs):
        placeholder = PLACEHOLDER[kwargs['type']]
        count = kwargs['count']
        content_list = kwargs['content']
        resource_list = kwargs['resource']
        sel = kwargs['selector']
        src = '@src'
        if 'src_attr' in kwargs:
            src = kwargs['src_attr']
        src = sel.css(kwargs['src']).xpath(src).extract()
        desc = ''
        if 'desc' in kwargs:
            desc = ''.join(sel.css(kwargs['desc']).extract()).strip()
        if len(src) > 1:
            for s in src:
                ref = placeholder.format(count)
                res = {'src': s, 'desc': desc, 'ref': ref}
                resource_list.append(res)
                content_list.append(ref)
                count += 1
            return count
        src = src[0]
        if not src:
            return count
        ref = placeholder.format(count)
        count += 1
        res = {'ref': ref, 'src': src, 'desc': desc}
        resource_list.append(res)
        content_list.append(res['ref'])
        return count