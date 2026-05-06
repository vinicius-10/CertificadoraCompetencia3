// login.js — Autenticação via Fetch + SweetAlert2

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("login-form").addEventListener("submit", (e) => {
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

    Swal.fire({
        title: "Entrando...",
        text: "Aguarde um momento.",
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => Swal.showLoading(),
    });

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ usuario, senha }),
        });

        const data = await response.json();

        if (response.ok && data.success) {
            window.location.href = data.redirect || "/";

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