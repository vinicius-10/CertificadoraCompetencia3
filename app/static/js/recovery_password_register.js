/**
 * Handles the password reset form submission.
 *
 * This script prevents the default form submission, collects the form data,
 * sends the password reset request to the backend API, and displays feedback to
 * the user through SweetAlert2.
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * Prevents the default form submission and starts the password reset flow.
     *
     * @param {SubmitEvent} e - Submit event triggered by the password reset form.
     * @returns {void}
     */
    document.getElementById("redefinicao-form").addEventListener("submit", (e) => {
        e.preventDefault();
        resetPassword(e.target);
    });

});



/**
 * Submits the password reset form data to the API.
 *
 * The function reads the current values from the password reset form, converts
 * them into a JSON payload, sends the data to the backend, and handles both
 * success and error responses with user-friendly alerts.
 *
 * @async
 * @function resetPassword
 * @description Input: none. The function reads data directly from the
 * password reset form in the DOM.
 * @returns {Promise<void>} Resolves when the password reset request has been
 * processed and the corresponding alert has been displayed.
 */
async function resetPassword(formReset){
    const formData = new FormData(formReset);
    /** @type {Record<string, FormDataEntryValue>} */
    const dataRegister = Object.fromEntries(formData.entries());

    const urlParams = new URLSearchParams(window.location.search);
    dataRegister.token = urlParams.get("token") || "";

    if (!validateForm(dataRegister)) {
        return;
    }

    Swal.fire({
        title: 'Carregando...',
        text: 'Por favor, aguarde',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    try{
        const response = await fetch("/api/auth/recovery_password", {
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
                title: "Senha atualizada",
                text: data.message || "Senha alterada com sucesso.",
                confirmButtonText: "Entrar",
            }).then( () => {
                window.location.href = data.redirect || "/login";
            });
        } else {
            Swal.fire({
                icon: "error",
                title: "Não foi possível redefinir a senha",
                text: data.message || "Verifique os dados e tente novamente.",
                confirmButtonText: "Tentar novamente",
            }).then( ()  =>{
                if(data.redirect){
                    window.location.href = data.redirect;
                }
            });
        }
    } catch(err) {
        Swal.close();
        Swal.fire({
            icon: "error",
            title: "Erro de conexão",
            text: "Não foi possível conectar ao servidor.",
            confirmButtonText: "Tentar novamente",
        });
        console.error("Erro na requisição de redefinição de senha:", err);
    }
}


/**
 * Validates the password reset form data before sending it to the API.
 *
 * The function checks whether both password fields were filled, whether the
 * two passwords match, and whether the new password respects the accepted
 * length range. When a validation fails, it shows a SweetAlert2 message with
 * feedback for the user.
 *
 * @param {Record<string, FormDataEntryValue>} data - Password reset form data.
 * @returns {boolean} `true` when the form data is valid; otherwise, `false`.
 */
function validateForm(data){
    const password = data.Nova_senha?.trim() || "";
    const passwordCheck = data.Confirmar_senha?.trim() || "";

    if (!password || !passwordCheck) {
        Swal.fire({
            icon: "error",
            title: "Campos obrigatórios",
            text: "Preencha todos os campos.",
            confirmButtonText: "Tentar novamente",
        });
        return false;
    }

    if(password !== passwordCheck){
        Swal.fire({
            icon: "error",
            title: "Senhas diferentes",
            text: "As senhas devem ser iguais.",
            confirmButtonText: "Tentar novamente",
        });
        return false;
    }

    if(password.length < 6){
        Swal.fire({
            icon: "error",
            title: "Senha muito pequena",
            text: "A senha deve ter 6 ou mais caracteres.",
            confirmButtonText: "Tentar novamente",
        });
        return false;
    }

    if(password.length >= 250){
        Swal.fire({
            icon: "error",
            title: "Senha muito grande",
            text: "A senha deve ter menos de 250 caracteres.",
            confirmButtonText: "Tentar novamente",
        });
        return false;
    }

    return true;
}
