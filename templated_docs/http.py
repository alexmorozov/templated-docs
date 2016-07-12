# --coding: utf8--

import os
import mimetypes

from django.http import HttpResponse


class FileResponse(HttpResponse):
    """
    One-time HTTP response with a generated file. DELETES A FILE AFTERWARDS!
    """
    def __init__(self, actual_file, visible_name, delete=True,
                 *args, **kwargs):
        super(FileResponse, self).__init__(*args, **kwargs)

        self['Content-type'] = mimetypes.guess_type(actual_file)[0]
        self['Content-disposition'] = 'attachment; filename=%s' % visible_name
        with open(actual_file, 'rb') as f:
            self.content = f.read()
        self['Content-length'] = len(self.content)
        if delete:
            os.unlink(actual_file)
