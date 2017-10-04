# --coding: utf8--

import os.path

from django.db.models.fields.files import ImageFieldFile
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django import template

register = template.Library()

class ImageNode(template.Node):

    def __init__(self, value):
        self.image_field = template.Variable(value)

        try:
            Img
        except:
            global Img
            from PIL import Image as Img # User should not be forced to install PIL if he does not utilize images


    def render(self, context):
        try:
            self.value = self.image_field.resolve(context)
            if not isinstance(self.value, ImageFieldFile):
                raise template.VariableDoesNotExist(
                    'Image argument should be an ImageField')
            images = context.dicts[0].setdefault('ootemplate_imgs', {})
            id = len(images)
            z_index = id + 3  # Magic
            x_dpi = Img.open(self.value.path).info['dpi'][0]
            y_dpi = Img.open(self.value.path).info['dpi'][1]
            width = self.value.width * 2.54/x_dpi
            height = self.value.height * 2.54/y_dpi
            filename = os.path.basename(self.value.name)
            basename = os.path.splitext(filename)[0]

            if context['img_category']:
                img_num = id + 1
                img_category = context['img_category']

                img_description = '%(img_category)s <text:sequence text:ref-name="refIllustration%(img_num)i" text:name="%(img_category)s" text:formula="ooow:Illustration+1" style:num-format="1">%(img_num)i</text:sequence>.'
            else:
                img_description = ''

            images[self.value.path] = self.value
            img_frame = '<draw:frame draw:style-name="gr%(z_index)s" ' \
                    'draw:name="%(basename)s" ' \
                    'draw:id="id%(id)s" ' \
                    'text:anchor-type="paragraph" svg:width="%(width)fcm" ' \
                    'svg:height="%(height)fcm" draw:z-index="%(z_index)s">' \
                    '<draw:image xlink:href="Pictures/%(filename)s" ' \
                    'xlink:type="simple" xlink:show="embed" ' \
                    'xlink:actuate="onLoad"/></draw:frame>'

            return (img_frame + img_description) % locals()
        except template.VariableDoesNotExist:
            return ''


@register.tag
def image(parser, token):
    """
    Insert an image from a ImageField into a document.
    """
    try:
        tag_name, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires a file as an argument' % tag_name)
    return ImageNode(value)


@register.filter
def lolinebreaks(value):
    """
    LibreOffice-flavored ``linebreaks`` filter.
    """
    if not value:
        return ''
    paragraphs = [line for line in escape(value).splitlines()]
    return mark_safe('<text:line-break/>'.join(paragraphs))