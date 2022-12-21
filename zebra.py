# coding=utf-8
import socket

from trytond.config import config as config_
from trytond.pool import Pool
from trytond.report import Report
from trytond.report.report import TranslateFactory
from trytond.transaction import Transaction

from jinja2 import Environment

# Determines the port of the Zebra Printer
ZEBRA_PORT = config_.getint('zebra', 'port', default=9100)

# Determines the host_name of the Zebra Printer
ZEBRA_HOST = config_.get('zebra', 'host_name', default='imp-label-1.saluc.com')


class ZebraReport(Report):

    def print_xml(xml_document, timeout=10):
        """
        Send XML formatted text to a network label printer
        :param xml_document: Document object, fully build for label.
        :param timeout: Socket timeout for printer connection, default 10.
        """

        printer_hostname = Transaction().context.get('printer_hostname')
        if not printer_hostname:
            printer_hostname = ZEBRA_HOST

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((printer_hostname, ZEBRA_PORT))
            s.send(bytes(xml_document, 'utf-8'))

    @classmethod
    def render(cls, report, report_context):
        pool = Pool()
        Translation = pool.get('ir.translation')
        Company = pool.get('company.company')

        report_content = (report.report_content if report.report_content
                          else False)

        if not report_content:
            raise Exception('Error', 'Missing report file!')

        # Make the report itself available in the report context
        report_context['report'] = report

        translate = TranslateFactory(cls.__name__, Translation)
        report_context['setLang'] = lambda language: translate.set_language(
            language)

        company_id = Transaction().context.get('company')
        report_context['company'] = Company(company_id)

        return cls.render_template(report_content, report_context, translate)

    @classmethod
    def execute(cls, ids, data):
        report_type, content, direct_print, name = super().execute(ids, data)
        cls.print_xml(content)
        return report_type, content, direct_print, name

    @classmethod
    def get_environment(cls):
        """
        Create and return a jinja environment to render templates
        Downstream modules can override this method to easily make changes
        to environment
        """
        env = Environment(
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=['jinja2.ext.loopcontrols'],
        )
        # env.filters.update(cls.get_jinja_filters())
        return env

    @classmethod
    def render_template(cls, template, localcontext, translator):
        """
        Render the template using Jinja2
        """
        env = cls.get_environment()

        report_template = env.from_string(template.decode('utf-8)'))
        return report_template.render(**localcontext)
