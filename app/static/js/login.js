// login.js — Autenticação via Fetch + SweetAlert2

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("login-form").addEventListener("submit", (e) => {
    console.log("Formulário de login submetido");
    e.preventDefault();
    login();
  });
});

async function login() {
    const usuario = document.getElementById("usuario").value.trim();
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
        const response = await fetch("/api/login", {
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
        Swal.fire({
            icon: "error",
            title: "Erro de conexão",
            text: "Não foi possível conectar ao servidor. Tente novamente.",
            confirmButtonText: "Ok",
        });
        console.error("Erro na requisição de login:", err);
    }
}