import logging

from safety.formatter import FormatterAPI
from safety.formatters.json import build_json_report
from safety.output_utils import get_report_brief_info, parse_junit
from safety.util import get_basic_announcements

LOG = logging.getLogger(__name__)


class JunitReport(FormatterAPI):
    """Junit report, for when the output is input for something else"""

    def render_vulnerabilities(self, announcements, vulnerabilities, remediations, full, packages, fixes=()):
        LOG.debug(
            f'Junit Output, Rendering {len(vulnerabilities)} vulnerabilities, {len(remediations)} package '
            f'remediations with full_report: {full}')
        report = build_json_report(announcements, vulnerabilities, remediations, packages)

        #Add junit stuff here
        report['junit']  = {}
        report['junit']['tests'] = report['report_meta']['packages_found'] + (report['report_meta']['vulnerabilities_found'] * 2) + report['report_meta']['vulnerabilities_ignored']
        report['junit']['skipped'] = report['report_meta']['vulnerabilities_ignored']
        report['junit']['failures'] = report['report_meta']['vulnerabilities_found'] * 2
        # ~ report['junit']['package_ignored_vulnerabilities'] = [ v['package_name'] for v in report['report_meta']['ignored_vulnerabilities'] ]
        # ~ report['junit']['package_vulnerabilities_found'] = [ v['package_name'] for v in report['report_meta']['vulnerabilities_found'] ]
        report['junit']['duration_per_test'] = report['report_meta']['duration'] / report['report_meta']['packages_found']

        return parse_junit(kwargs={"json_data": report})

    def render_licenses(self, announcements, licenses):
        pass

    def render_announcements(self, announcements):
        pass
