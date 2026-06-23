// login.js — Autenticação via Fetch + SweetAlert2



document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("login-form").addEventListener("submit", (e) => {
        e.preventDefault();
        login();
    });

    document.getElementById('usuario').addEventListener('input', (e) => {
        masckaraCPF(e);
    });
});



async function login() {
    const usuario = document.getElementById("usuario").value.replace(/[^\d]+/g, '').trim();
    const senha = document.getElementById("senha").value.trim();

    if (!usuario || !senha) {
        Swal.fire({
            icon: "warning",
            title: "Campos obrigatórios",
            text: "Preencha o usuário e a senha antes de continuar.",
            confirmButtonText: "Ok",
        });
        return;
    }

    if (validateCPF(usuario)) {
       

        const urlParams = new URLSearchParams(window.location.search);
        const nextUrl = urlParams.get("next");

        Swal.fire({
            title: "Entrando...",
            text: "Aguarde um momento.",
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => Swal.showLoading(),
        });

        try {
            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest" 
                },
                body: JSON.stringify({ 
                    usuario, 
                    senha,
                    next_url: nextUrl 
                }),
            });
            
            const data = await response.json();
            Swal.close();
            
            if (response.ok && data.success) {
                
                window.location.href = data.redirect;
            } else {
                Swal.fire({
                    icon: "error",
                    title: "Falha no login",
                    text: data.message || "Usuário ou senha incorretos.",
                    confirmButtonText: "Tentar novamente",
                });
            }

        } catch (err) {
            Swal.close();
            Swal.fire({
                icon: "error",
                title: "Erro de conexão",
                text: "Não foi possível conectar ao servidor. Tente novamente.",
                confirmButtonText: "Ok",
            });
            console.error("Erro na requisição de login:", err);
        }
    } else {
        Swal.fire({
            icon: "error",
            title: "CPF inválido",
            text: "Por favor, insira um CPF válido.",
            confirmButtonText: "Ok",
        });
    }
}


function masckaraCPF(e) {
    let value = e.target.value;

    if (value.length > 14) {
        value = value.slice(0, 14);
    }
    value = value.replace(/\D/g, '');

    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    
    e.target.value = value;
}


function validateCPF(cpf) {
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) {
        return false;
    }

    let sum = 0;
    for(let c = 9; c <= 10; c++) {
        sum = 0;
        for (let i = 0; i < c; i++) {
            sum += parseInt(cpf.charAt(i)) * (c+1 - i);
        }
        let remainder = (sum * 10) % 11;
        if (remainder >= 10) {
            remainder = 0;
        }
        if (remainder !== parseInt(cpf.charAt(c))) {
            return false;
        }
    }
    return true;
}