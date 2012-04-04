import os
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def collect_static():
    cmd = 'python manage.py collectstatic -v0 --noinput'
    result = os.system(cmd)
    print "-- helpers -- colect_static() -- result: " + str(result)

def generate_pdf(request, advert_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=advert.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response