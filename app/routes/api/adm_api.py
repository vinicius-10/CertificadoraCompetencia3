from urllib.parse import urlencode

from flask import Blueprint, render_template, request, make_response, url_for

from app.services import generate_users_report_csv, generate_users_report_pdf, search_users as search_users_service

adm_api_bp = Blueprint('adm_api', __name__)


def _make_hx_redirect_response():
    query_string = urlencode(request.args.to_dict(flat=True))
    redirect_url = url_for(request.endpoint)

    if query_string:
        redirect_url = f"{redirect_url}?{query_string}"

    response = make_response("", 200)
    response.headers['HX-Redirect'] = redirect_url
    return response


@adm_api_bp.route("/search_users", methods=['GET'])
def search_users():
    volunteers = search_users_service(request.args)
    return render_template('users_list.html', volunteers=volunteers)


@adm_api_bp.route("report/pdf", methods=['GET'])
def report_pdf():
    if request.headers.get('HX-Request'):
        return _make_hx_redirect_response()

    pdf_bytes = generate_users_report_pdf(request.args)
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_voluntarios.pdf'
    
    return response


@adm_api_bp.route("report/csv", methods=['GET'])
def report_csv():
    if request.headers.get('HX-Request'):
        return _make_hx_redirect_response()

    csv_bytes = generate_users_report_csv(request.args)
    response = make_response(csv_bytes)
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_voluntarios.csv'

    return response
