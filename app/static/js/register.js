/**
 * Handles the user registration form submission.
 *
 * This script prevents the default form submission, collects the form data,
 * sends the registration request to the backend API, and displays feedback to
 * the user through SweetAlert2.
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * Prevents the default form submission and starts the registration flow.
     *
     * @param {SubmitEvent} e - Submit event triggered by the registration form.
     * @returns {void}
     */
    document.getElementById("cadastro-form").addEventListener("submit", (e) => {
        e.preventDefault();
        register();
    });
});


/**
 * Submits the registration form data to the user registration API.
 *
 * The function reads the current values from the registration form, converts
 * them into a JSON payload, sends the data to the backend, and handles both
 * success and error responses with user-friendly alerts.
 *
 * @async
 * @function register
 * @description Input: none. The function reads data directly from the
 * registration form in the DOM.
 * @returns {Promise<void>} Resolves when the registration request has been
 * processed and the corresponding alert has been displayed.
 */
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
        /** @type {Record<string, FormDataEntryValue>} */
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
                title: "Usuario cadastrado",
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
    } catch(err) {
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
