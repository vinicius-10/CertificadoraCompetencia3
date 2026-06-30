"""Service functions for admin searches and user report generation."""

import csv
from io import StringIO
from datetime import datetime, timezone

from flask import render_template
from sqlalchemy import select, or_
from weasyprint import HTML

from app.models import User, db, UserStatus, UserSector, UserPosition, UserProfile


def _build_users_query(filters):
    """
    Build the base user query used by admin listings and reports.

    The accepted filters mirror the query parameters sent by the admin page:
    free-text search by name, active/all users, sector, position, profile, and
    sorting. Sorting is restricted to a fixed map of known columns to avoid
    using arbitrary user-provided field names in the query.

    Args:
        filters (Mapping): Query parameters from the admin interface.

    Returns:
        tuple: A SQLAlchemy ``Select`` statement and a boolean indicating
            whether inactive users are included in the result set.
    """
    search_query = filters.get('q', '').strip()
    all_user = filters.get('todos', 'false') == 'true'
    sector_filter = UserSector.from_string(filters.get('setor', ''))
    position_filter = UserPosition.from_string(filters.get('cargo', ''))
    profile_filter = UserProfile.from_string(filters.get('tipo', ''))
    sort_by = filters.get('sort_by', 'entry_at')
    sort_dir = filters.get('sort_dir', 'asc')

    stmt = select(User)

    if not all_user:
        stmt = stmt.where(User.status == UserStatus.ACTIVE)
    else:
         stmt = stmt.where(User.status != UserStatus.DELETED)

    if search_query:
        stmt = stmt.where(
            or_(
                User.name.ilike(f"%{search_query}%"),
                User.code_institutional.ilike(f"%{search_query}%")
            )
        )

    if sector_filter:
        stmt = stmt.where(User.sector == sector_filter)

    if position_filter:
        stmt = stmt.where(User.position == position_filter)

    if profile_filter:
        stmt = stmt.where(User.profile == profile_filter)

    sort_columns = {
        'name': User.name,
        'sector': User.sector,
        'position': User.position,
        'entry_at': User.entry_at,
        'departure_at': User.departure_at,
        'profile': User.profile,
    }
    sort_column = sort_columns.get(sort_by, User.entry_at)

    if sort_dir == 'desc':
        stmt = stmt.order_by(sort_column.desc())
    else:
        stmt = stmt.order_by(sort_column.asc())

    return stmt, all_user


def search_users(filters):
    """
    Search users using the filters sent by the admin interface.

    This function is used by the HTMX-powered admin table. It returns model
    objects so the API route can render the table partial.

    Args:
        filters (Mapping): Query parameters containing optional search text,
            sector, position, profile, active/all visibility, and sorting
            options.

    Returns:
        list[User]: Users matching the requested filters.
    """
    stmt, _ = _build_users_query(filters)
    return db.session.scalars(stmt).all()


def generate_users_report_pdf(filters):
    """
    Generate the PDF report for users matching the admin filters.

    The report contains the same filtered and sorted users shown in the admin
    table, rendered through the ``report_pdf.html`` template and converted to
    PDF using WeasyPrint.

    Args:
        filters (Mapping): Query parameters containing optional search text,
            sector, position, profile, active/all visibility, and sorting
            options.

    Returns:
        bytes: Rendered PDF bytes ready to be returned in an HTTP response.
    """
    stmt, all_user = _build_users_query(filters)
    volunteers = db.session.scalars(stmt).all()

    type_report = "todos voluntários" if all_user else "voluntários ativos"
    date = datetime.now(timezone.utc).strftime('%d/%m/%Y')

    html_rendered = render_template(
        'report_pdf.html',
        volunteers=volunteers,
        date=date,
        type_report=type_report,
    )

    return HTML(string=html_rendered).write_pdf()


def generate_users_report_csv(filters):
    """
    Generate the CSV report for users matching the admin filters.

    The CSV uses semicolon delimiters and UTF-8 with BOM so spreadsheet tools
    commonly used in Portuguese locales open the file with accented characters
    and columns correctly.

    Args:
        filters (Mapping): Query parameters containing optional search text,
            sector, position, profile, active/all visibility, and sorting
            options.

    Returns:
        bytes: UTF-8 CSV bytes ready to be returned in an HTTP response.
    """
    stmt, _ = _build_users_query(filters)
    volunteers = db.session.scalars(stmt).all()

    csv_file = StringIO()
    writer = csv.writer(csv_file, delimiter=';')

    writer.writerow([
        "Nome",
        "Código institucional",
        "Email",
        "Setor",
        "Cargo",
        "Perfil",
        "Entrada",
        "Saída",
        "Status",
    ])

    for volunteer in volunteers:
        writer.writerow([
            volunteer.name,
            volunteer.code_institutional or "",
            volunteer.email,
            volunteer.sector.value if volunteer.sector else "",
            volunteer.position.value if volunteer.position else "",
            volunteer.profile.value if volunteer.profile else "",
            volunteer.entry_at.strftime('%d/%m/%Y') if volunteer.entry_at else "",
            volunteer.departure_at.strftime('%d/%m/%Y') if volunteer.departure_at else "",
            volunteer.status.value if volunteer.status else "",
        ])

    return csv_file.getvalue().encode('utf-8-sig')
