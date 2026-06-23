document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("recuperacao-form").addEventListener("submit", (e) => {
        e.preventDefault();
        register();
    });
});


async function register(){
    const email = document.getElementById("email-recuperacao").value;
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    if(regex.test(email)){
        Swal.fire({
            title: 'Carregando...',
            text: 'Por favor, aguarde',
            allowOutsideClick: false,
            didOpen: () => {
            Swal.showLoading();
            }
        });
        try {
            const response = await fetch("/api/auth/recovery", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest" 
                },
                body: JSON.stringify({ 
                    email, 
                }),
            });
                
            const data = await response.json();
            Swal.close();
            
            if (response.ok && data.success) {
                
                Swal.fire({
                    icon: "success",
                    title: "Email enviado",
                    text: data.message || "Caso o e-mail esteja cadastrado, um link de redefinição foi enviado. Lembre-se de verificar a pasta de spam.",
                    confirmButtonText: "Fechar",
                });
            } else {
                Swal.fire({
                    icon: "error",
                    title: "Falha no login",
                    text: data.message || "Não foi possível enviar o e-mail. Tente novamente mais tarde.",
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
    }else{
        Swal.fire({
            icon: "error",
            title: "Email invalido",
            text: "Verifique o email.",
            confirmButtonText: "Ok",
        });

    }
    
    

    

}