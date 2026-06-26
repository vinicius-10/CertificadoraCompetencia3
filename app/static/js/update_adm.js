/**
 * Handles the user update form submission.
 *
 * This script prevents the default form submission, collects the form data,
 * sends the update request to the backend API, and displays feedback to
 * the user through SweetAlert2.
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * Prevents the default form submission and starts the update flow.
     *
     * @param {SubmitEvent} e - Submit event triggered by the update form.
     * @returns {void}
     */
    document.getElementById("cadastro-form").addEventListener("submit", (e) => {
        e.preventDefault();
        update();
    });
});


/**
 * Submits the update form data to the user update API.
 *
 * The function reads the current values from the update form, converts
 * them into a JSON payload, sends the data to the backend, and handles both
 * success and error responses with user-friendly alerts.
 *
 * @async
 * @function update
 * @description Input: none. The function reads data directly from the
 * update form in the DOM.
 * @returns {Promise<void>} Resolves when the update request has been
 * processed and the corresponding alert has been displayed.
 */
async function update(){
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

        const response = await fetch("/api/user/update_adm", {
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
                title: "Atualização concluida",
                text: data.message || "Usuario atualizado realizado com sucesso.",
                confirmButtonText: "Fechar",
            });
        } else {
            Swal.fire({
                icon: "error",
                title: "Falha na atualização",
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
