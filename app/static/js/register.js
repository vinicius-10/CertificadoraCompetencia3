document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("cadastro-form").addEventListener("submit", (e) => {
        e.preventDefault();
        register();
    });
});


async function register(){
    const form_register = document.getElementById("cadastro-form");
    console.log("formulario:" + form_register.Nome.value);

    Swal.fire({
        title: 'Carregando...',
        text: 'Por favor, aguarde',
        allowOutsideClick: false,
        didOpen: () => {
        Swal.showLoading();
        }
    });
    
    try{
        const formData = new FormData(form_register);
        const dataRegister = Object.fromEntries(formData.entries());
        console.log("form data:", dataRegister);

        const response = await fetch("/api/user/register", {
            method: 'POST',
            headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest" 
                },
            body: JSON.stringify(dataRegister)
        });

        const data = await response.json();
        Swal.close();
            
        if (response.ok && data.success) {
            
            Swal.fire({
                icon: "success",
                title: "Email enviado",
                text: data.message || "Cadastro realizado com sucesso.",
                confirmButtonText: "Fechar",
            });
        } else {
            Swal.fire({
                icon: "error",
                title: "Falha no cadastro",
                text: data.message || "Verifique os dados.",
                confirmButtonText: "Tentar novamente",
            });
        }
    }catch(err){
        Swal.close();
        Swal.fire({
            icon: "error",
            title: "Erro de conexão",
            text: "Não foi possível conectar ao servidor.",
            confirmButtonText: " Tente novamente",
        });
        console.error("Erro na requisição de login:", err);
}

}
