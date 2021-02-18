import calendar
import logging
from collections import defaultdict
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML

from .models import Tblpermit, Transaction

LOG_FORMAT = "%(Levelname)s:%(asctime)s:%(message)s"
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


@login_required(login_url="/accounts/login")
class Library:
    def getdates(start_year, start_month):
        rist = []
        di = []
        asd = Transaction.objects.all().filter(business_date__year=start_year).filter(
            business_date__month=start_month).values("business_date", "pos_name").distinct()
        for a in asd:
            dictio = a["pos_name"], a["business_date"].strftime("%m-%d-%Y")
            rist.append(dictio)
        d = defaultdict(list)
        for year, month in rist:
            d[year].append(month)
        for k, v in d.items():
            dictq = {"pc": k, "business_date": v}
            di.append(dictq)
        return di

    def getdaysinmonth(start_year, start_month):
        num = calendar.monthrange(int(start_year), int(start_month))[1]
        days = [date(int(start_year), int(start_month), day) for day in range(1, num + 1)]
        return days

    def timeanddateconversion(data):
        return datetime.strptime(data, '%m/%d/%Y').strftime('%Y-%m-%d')

    def twelvehourto24hr(self):
        return datetime.strptime(self, "%I:%M:%S %p").strftime("%H:%M:%S")

    def reportGeneration(context, name, url):
        html_template = get_template(url).render(context)
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{}.pdf"'.format(name)
        return response
        # html_string = render_to_string(url, context)
        # html = HTML(string=html_string)
        # result = html.write_pdf()
        # response = HttpResponse(content_type='application/pdf;')
        # response['Content-Disposition'] = ('inline; filename="{}.pdf"'.format(name))
        # response['Content-Transfer-Encoding'] = 'binary'
        # with tempfile.NamedTemporaryFile(delete=True) as output:
        #     output.write(result)
        #     output.flush()
        #     output = open(output.name, 'rb')
        #     response.write(output.read())
        # return response

    def getposnotinlist():
        try:
            get_pos_name = Tblpermit.objects.values_list('pc', flat=True)
            get_pos_name_transact = list(Transaction.objects.values_list("pos_name", flat=True).distinct())
            pos_name_as_list = list(get_pos_name)

            for item in get_pos_name_transact:
                if item in get_pos_name_transact:
                    pos_name_as_list.remove(item)
                else:
                    print("none")
            return pos_name_as_list
        except Exception as e:
            logger.info(e)
