from flask import render_template, Blueprint, jsonify
from models import db, User, UserProfile, UserStatus, UserMarital
import os
test_bp = Blueprint('test', __name__)



@test_bp.route("/basic-user")
def teste_bd():
    try:
        ra = "40000"
        email = 'teste4@teste.com'
        cpf = '40000000000'
        rg = '400000000'
        
        user_exists = User.query.filter_by(ra=ra).first()
        if user_exists:
            return {"status": "success", "message": "Usuario ja existe"}, 200
        
        new_user = User(
            ra=ra,
            password="senha123",
            name="João Silva",
            email=email,
            cpf=cpf,
            rg=rg,
            nationality='Brasileiro',
            marital=UserMarital.SINGLE,
            profession='Teste',
            profile=UserProfile.ADMIN,
            status=UserStatus.ACTIVE
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {"status": "success", "message": "Usuario criado com sucesso"}, 201
        
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e),"data": None}, 500
        

@test_bp.route("/test")
def test():
    variavel = os.environ.get('SECRET_KEY', 'Valor padrão se a variável não estiver definida')
    return render_template("test.html", name=variavel)


