document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("cadastro-form").addEventListener("submit", (e) => {
        e.preventDefault();
        register();
    });
});


async function register(){
    const form_register = document.getElementById("cadastro-form");
    console.log("formulario:" + form_register.name.value);

    Swal.fire({
        title: 'Carregando...',
        text: 'Por favor, aguarde',
        allowOutsideClick: false,
        didOpen: () => {
        Swal.showLoading();
        }
    });
    
    $fd = new FormData(form_register);

    const response = await fetch("/api/user/register", {
        method: 'POST',
        body: $fd
    });

}