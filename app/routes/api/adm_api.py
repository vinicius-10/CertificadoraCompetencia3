"""API endpoints for admin user search and report downloads."""

from urllib.parse import urlencode

from flask import Blueprint, render_template, request, make_response, url_for

from app.services import generate_users_report_csv, generate_users_report_pdf, search_users as search_users_service

adm_api_bp = Blueprint('adm_api', __name__)


def _make_hx_redirect_response():
    """
    Build an HTMX redirect response that preserves the current query filters.

    Report download buttons are triggered through HTMX so they can include the
    current filter inputs. Since HTMX would otherwise try to inject the binary
    report response into the page, this helper redirects the browser to the
    same endpoint with the current query string. The redirected non-HTMX
    request then performs the actual file download.

    Returns:
        Response: Empty HTTP response containing the ``HX-Redirect`` header.
    """
    query_string = urlencode(request.args.to_dict(flat=True))
    redirect_url = url_for(request.endpoint)

    if query_string:
        redirect_url = f"{redirect_url}?{query_string}"

    response = make_response("", 200)
    response.headers['HX-Redirect'] = redirect_url
    return response


@adm_api_bp.route("/search_users", methods=['GET'])
def search_users():
    """
    Render the filtered user list used by the admin dashboard.

    Query parameters may include search text, sector, position, user profile,
    active/all user visibility, and sorting options. The filtering and sorting
    rules are delegated to the admin service.

    Returns:
        str: Rendered ``users_list.html`` partial containing the matched users.
    """
    volunteers = search_users_service(request.args)
    return render_template('users_list.html', volunteers=volunteers)


@adm_api_bp.route("report/pdf", methods=['GET'])
def report_pdf():
    """
    Download a PDF report for users matching the current admin filters.

    When called by HTMX, the route returns an ``HX-Redirect`` response so the
    browser performs a normal request and downloads the PDF file. Non-HTMX
    requests generate and return the PDF directly.

    Returns:
        Response: Either an HTMX redirect response or a PDF file response.
    """
    if request.headers.get('HX-Request'):
        return _make_hx_redirect_response()

    pdf_bytes = generate_users_report_pdf(request.args)
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_voluntarios.pdf'
    
    return response


@adm_api_bp.route("report/csv", methods=['GET'])
def report_csv():
    """
    Download a CSV report for users matching the current admin filters.

    When called by HTMX, the route returns an ``HX-Redirect`` response so the
    browser performs a normal request and downloads the CSV file. Non-HTMX
    requests generate and return the CSV directly.

    Returns:
        Response: Either an HTMX redirect response or a CSV file response.
    """
    if request.headers.get('HX-Request'):
        return _make_hx_redirect_response()

    csv_bytes = generate_users_report_csv(request.args)
    response = make_response(csv_bytes)
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_voluntarios.csv'

    return response
