# -*- coding: utf-8 -*-

import multiprocessing
import os.path
import re
from tempfile import NamedTemporaryFile
import zipfile

from django.conf import settings
from django.template import Template

try:
    # Django 1.9+
    from django.template.exceptions import TemplateDoesNotExist
except ImportError:
    from django.template import TemplateDoesNotExist

from django.template import Context, engines

from django.utils.encoding import smart_bytes, smart_str

from pylokit import Office

import logging
log = logging.getLogger(__name__)

__version__ = '0.3.3'


IMAGES_CONTEXT_KEY = '_templated_docs_imgs'


def _get_template_loaders():
    """
    Get all available template loaders for the Django engine.
    """
    loaders = []

    for loader_name in engines['django'].engine.loaders:
        loader = engines['django'].engine.find_template_loader(loader_name)
        if loader is not None and hasattr(loader, 'get_template_sources'):
            loaders.append(loader)
    return tuple(loaders)


def fix_inline_tags(content):
    """
    Replace broken entities within Django template constructs.

    MS Word likes to replace some entities just in case, and we end up with
    broken Django constructs. To remedy that, we find all the Django tags and
    variables and fix entities inside them.
    """
    def repl(match):
        text = match.group(0)
        text = text.replace('<text:s/>', ' ')
        text = text.replace('&apos;', "'")
        text = text.replace('&quot;', '"')
        return re.sub(r'<[^>]+>', '', text)

    django_tag_re = r'(\{[\{\%].+?[\%\}]\})'
    return re.sub(django_tag_re, repl, content)


def find_template_file(template_name):
    """
    Return a full path to the specified template file.

    The key difference from the stock `find_template` is that we don't try to
    load a template in memory, because we'll deal with it ourselves.
    """
    for loader in _get_template_loaders():
        for origin in loader.get_template_sources(template_name, None):
            path = getattr(origin, 'name', origin)  # Django <1.9 compatibility
            if os.path.exists(path):
                return path
    raise TemplateDoesNotExist(template_name)


def _convert_file(filename, format, result_queue=None, options=None):
    """Helper function to convert a file via LOKit.

    This function can be called via subprocess so that in the event of LO
    crashing randomly after conversion, it will not terminate the parent
    process. This is assisted by inserting the result into a Queue object.
    """
    lo_path = getattr(
        settings,
        'TEMPLATED_DOCS_LIBREOFFICE_PATH',
        '/usr/lib/libreoffice/program/')

    with Office(lo_path) as lo:
        conv_file = NamedTemporaryFile(delete=False,
                                       suffix='.%s' % format)
        with lo.documentLoad(filename) as doc:
            doc.saveAs(str(conv_file.name), options=options)
        os.unlink(filename)

    # type comparison is required instead of isinstance owing to
    # multiprocessing.Queue is a method
    if type(result_queue) == multiprocessing.queues.Queue:
        result_queue.put(conv_file.name)
    else:
        return conv_file.name


def fill_template(
    template_name,
    context,
    output_format='odt',
    options=None,
    separate_process=True,
):
    """Fill a document with data and convert it to the requested format.

    Returns an absolute path to the generated file.

    Supported output format:
        Text documents: doc, docx, fodt, html, odt, ott, pdf, txt, xhtml, png
        Spreadsheets: csv, fods, html, ods, ots, pdf, xhtml, xls, xlsx, png
        Presentations: fodp, html, odg, odp, otp, pdf, potm, pot, pptx, pps,
                       ppt, svg, swf, xhtml, png
        Drawings: fodg, html, odg, pdf, svg, swf, xhtml, png

    More on filter options,
    https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options  # noqa: E501

    :param template_name: the path to template, in OpenDocument format
    :param context: the context to be used to inject content
    :param output_format: the output format
    :param options: value of filterOptions in libreofficekit
    :param separate_process: allow LO to

    :return:
    """

    if not isinstance(context, Context):
        context = Context(context)

    context['output_format'] = output_format

    source_file = find_template_file(template_name)
    source_extension = os.path.splitext(source_file)[1]
    source = zipfile.ZipFile(source_file, 'r')

    dest_file = NamedTemporaryFile(delete=False, suffix=source_extension)
    dest = zipfile.ZipFile(dest_file, 'w')

    manifest_data = ''
    for name in source.namelist():
        data = source.read(name)
        if name.endswith('.xml'):
            data = smart_str(data)

        if any(name.endswith(file) for file in ('content.xml', 'styles.xml')):
            template = Template(fix_inline_tags(data))
            data = template.render(context)
        elif name == 'META-INF/manifest.xml':
            manifest_data = data[:-20]  # Cut off the closing </manifest> tag
            continue  # We will append it at the very end
        dest.writestr(name, smart_bytes(data))

    for _, image in context.dicts[0].get(IMAGES_CONTEXT_KEY, {}).items():
        filename = os.path.basename(image.name)
        ext = os.path.splitext(filename)[1][1:]
        manifest_data += ('<manifest:file-entry '
                          'manifest:media-type="image/%(ext)s" '
                          'manifest:full-path="Pictures/%(filename)s"/>\n'
                          ) % locals()
        image.open()
        dest.writestr('Pictures/%s' % filename, image.read())
        image.close()

    manifest_data += '</manifest:manifest>'
    dest.writestr('META-INF/manifest.xml', manifest_data)

    source.close()
    dest.close()

    if source_extension[1:] != output_format:
        if separate_process:
            results = multiprocessing.Queue()
            converter = multiprocessing.Process(
                target=_convert_file,
                args=(str(dest_file.name), output_format, results, options),
            )
            converter.start()
            return results.get()
        else:
            return _convert_file(
                filename=str(dest_file.name),
                format=output_format,
                options=options,
            )
    else:
        return dest_file.name
