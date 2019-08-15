import httplib


import flask_restful
from flask import jsonify

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.services.reporting.report import ReportService
from monkey_island.cc.services.reporting.zero_trust_service import ZeroTrustService

ZERO_TRUST_REPORT_TYPE = "zero_trust"
GENERAL_REPORT_TYPE = "general"
REPORT_TYPES = [GENERAL_REPORT_TYPE, ZERO_TRUST_REPORT_TYPE]

REPORT_DATA_PILLARS = "pillars"
REPORT_DATA_FINDINGS = "findings"
REPORT_DATA_DIRECTIVES_STATUS = "directives"

__author__ = ["itay.mizeretz", "shay.nehmad"]


class Report(flask_restful.Resource):

    @jwt_required()
    def get(self, report_type=GENERAL_REPORT_TYPE, report_data=None):
        if report_type == GENERAL_REPORT_TYPE:
            return ReportService.get_report()
        elif report_type == ZERO_TRUST_REPORT_TYPE:
            if report_data == REPORT_DATA_PILLARS:
                return jsonify({
                        "summary": ZeroTrustService.get_pillars_summary(),
                        "grades": ZeroTrustService.get_pillars_grades()
                    }
                )
            elif report_data == REPORT_DATA_DIRECTIVES_STATUS:
                return jsonify(ZeroTrustService.get_directives_status())
            elif report_data == REPORT_DATA_FINDINGS:
                return jsonify(ZeroTrustService.get_all_findings())

        flask_restful.abort(httplib.NOT_FOUND)