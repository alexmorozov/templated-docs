#--coding: utf8--

from django.shortcuts import render

from example.forms import SampleForm

from templated_docs import fill_template
from templated_docs.http import FileResponse


def sample_view(request):
    form = SampleForm(request.POST or None)

    if form.is_valid():
        doctype = form.cleaned_data['output_format']
        filename = fill_template(
            'sample.odt', form.cleaned_data,
            output_format=doctype)
        visible_filename = 'yummy.{}'.format(doctype)

        return FileResponse(filename, visible_filename)
    else:
        return render(request, 'index.html', {'form': form})
