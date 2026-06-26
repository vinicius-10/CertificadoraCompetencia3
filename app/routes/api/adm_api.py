from flask import Blueprint, render_template, request, make_response
from sqlalchemy import select
from weasyprint import HTML

from app.models import User, db, UserStatus, UserSector, UserPosition, UserProfile

adm_api_bp = Blueprint('adm_api', __name__)


@adm_api_bp.route("/search_users", methods=['GET'])
def search_users():
    search_query = request.args.get('q', '').strip()
    all_user = request.args.get('todos', 'false') == 'true'
    sector_filter =  UserSector.from_string(request.args.get('setor', ''))
    position_filter = UserPosition.from_string(request.args.get('cargo', ''))
    profile_filter = UserProfile.from_string(request.args.get('tipo', ''))

    stmt = select(User)

    if not all_user:
        stmt = stmt.where(User.status == UserStatus.ACTIVE)

    if search_query:
        stmt = stmt.where(User.name.ilike(f"%{search_query}%"))

    if sector_filter:
        stmt = stmt.where(User.sector == sector_filter)
        
    if position_filter:
        stmt = stmt.where(User.position == position_filter)
        
    if profile_filter:
        stmt = stmt.where(User.profile == profile_filter)

    stmt = stmt.order_by(User.entry_at.asc())

    volunteers = db.session.scalars(stmt).all()

    return render_template('users_list.html', volunteers=volunteers)


@adm_api_bp.route("report/pdf", methods=['GET'])
def report_pdf():
    search_query = request.args.get('q', '').strip()
    all_user = request.args.get('todos', 'false') == 'true'
    sector_filter =  UserSector.from_string(request.args.get('setor', ''))
    position_filter = UserPosition.from_string(request.args.get('cargo', ''))
    profile_filter = UserProfile.from_string(request.args.get('tipo', ''))

    stmt = select(User)

    if not all_user:
        stmt = stmt.where(User.status == UserStatus.ACTIVE)

    if search_query:
        stmt = stmt.where(User.name.ilike(f"%{search_query}%"))

    if sector_filter:
        stmt = stmt.where(User.sector == sector_filter)
        
    if position_filter:
        stmt = stmt.where(User.position == position_filter)
        
    if profile_filter:
        stmt = stmt.where(User.profile == profile_filter)

    stmt = stmt.order_by(User.entry_at.asc())

    volunteers = db.session.scalars(stmt).all()
    
    html_rendered = render_template(
        'report_pdf.html', 
        volunteers=volunteers
    )

    pdf_bytes = HTML(string=html_rendered).write_pdf()

    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_voluntarios.pdf'
    
    return response