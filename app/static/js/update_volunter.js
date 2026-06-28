/**
 * Handles the volunteer user update form submission.
 *
 * This script validates the update form, sends the update request to the
 * backend API, and displays feedback through SweetAlert2.
 */
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("cadastro-form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        update(e.target);
    });
});


/**
 * Submits the update form data to the volunteer user update API.
 *
 * @async
 * @param {HTMLFormElement} formUpdate - Update form submitted by the user.
 * @returns {Promise<void>} Resolves when the update request has been processed.
 */
async function update(formUpdate){
    const formData = new FormData(formUpdate);
    /** @type {Record<string, FormDataEntryValue>} */
    const dataUpdate = Object.fromEntries(formData.entries());

    /**
    if (!validateForm(dataUpdate)) {
        return;
    }
    */
    Swal.fire({
        title: 'Carregando...',
        text: 'Por favor, aguarde',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    try{
        const response = await fetch("/api/user/updateUser", {
            method: 'POST',
            headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest" 
                },
            body: JSON.stringify(dataUpdate)
        });

        const data = await response.json();
        Swal.close();
            
        if (response.ok && data.success) {
            Swal.fire({
                icon: "success",
                title: "Atualização concluída",
                text: data.message || "Usuário atualizado com sucesso.",
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
            confirmButtonText: "Tentar novamente",
        });
        console.error("Erro na requisição de atualização:", err);
    }
}


/**
 * Validates volunteer update form data before sending it to the API.
 *
 * @param {Record<string, FormDataEntryValue>} data - Update form data.
 * @returns {boolean} `true` when the form data is valid; otherwise, `false`.
 */
function validateForm(data){
    const values = normalizeFormData(data);

    const requiredFields = [
        ["Nome", "Nome"],
        ["Email", "Email"],
        ["Profissao", "Profissão"],
        ["Estado_Civil", "Estado civil"],
        ["Nacionalidade", "Nacionalidade"],
        ["Registro_Academico", "Registro acadêmico"],
        ["Logradouro", "Logradouro"],
        ["Bairro", "Bairro"],
        ["CEP", "CEP"],
        ["Numero", "Número"],
        ["Cidade", "Cidade"],
        ["Estado", "Estado"],
        ["Pais", "País"],
    ];

    const missingField = requiredFields.find(([fieldName]) => !values[fieldName]);
    if (missingField) {
        showValidationError("Campos obrigatórios", `Preencha o campo ${missingField[1]}.`);
        return false;
    }

    if (!isLettersAndSpaces(values.Nome)) {
        showValidationError("Nome inválido", "O nome deve conter apenas letras.");
        return false;
    }

    if (!isValidEmail(values.Email)) {
        showValidationError("Email inválido", "Informe um email válido.");
        return false;
    }

    if (!isLettersAndSpaces(values.Profissao) || values.Profissao.length > 100) {
        showValidationError("Profissão inválida", "A profissão deve conter apenas letras e ter até 100 caracteres.");
        return false;
    }

    if (!isLettersAndSpaces(values.Nacionalidade) || values.Nacionalidade.length > 50) {
        showValidationError("Nacionalidade inválida", "A nacionalidade deve conter apenas letras e ter até 50 caracteres.");
        return false;
    }

    if (!isDigits(values.Registro_Academico) || values.Registro_Academico.length > 20) {
        showValidationError("Registro acadêmico inválido", "O registro acadêmico deve conter apenas números e ter até 20 caracteres.");
        return false;
    }

    if (!isLettersAndSpaces(values.Logradouro) || values.Logradouro.length > 150) {
        showValidationError("Logradouro inválido", "O logradouro deve conter apenas letras e ter até 150 caracteres.");
        return false;
    }

    if (!isLettersAndSpaces(values.Bairro) || values.Bairro.length > 100) {
        showValidationError("Bairro inválido", "O bairro deve conter apenas letras e ter até 100 caracteres.");
        return false;
    }

    if (!isDigits(values.CEP) || values.CEP.length !== 8) {
        showValidationError("CEP inválido", "O CEP deve conter 8 números.");
        return false;
    }

    if (!isDigits(values.Numero) || values.Numero.length > 20) {
        showValidationError("Número inválido", "O número deve conter apenas números e ter até 20 caracteres.");
        return false;
    }

    if (!isLettersAndSpaces(values.Cidade) || values.Cidade.length > 100) {
        showValidationError("Cidade inválida", "A cidade deve conter apenas letras e ter até 100 caracteres.");
        return false;
    }

    if (!isLettersAndSpaces(values.Estado) || values.Estado.length > 100) {
        showValidationError("Estado inválido", "O estado deve conter apenas letras e ter até 100 caracteres.");
        return false;
    }

    if (!isLettersAndSpaces(values.Pais) || values.Pais.length > 50) {
        showValidationError("País inválido", "O país deve conter apenas letras e ter até 50 caracteres.");
        return false;
    }

    if (values.Complemento && (!isLettersNumbersAndSpaces(values.Complemento) || values.Complemento.length > 100)) {
        showValidationError("Complemento inválido", "O complemento deve conter apenas letras e números e ter até 100 caracteres.");
        return false;
    }

    if (!isValidPasswordChange(values.Nova_senha, values.Confirma_Senha)) {
        return false;
    }

    return true;
}


/**
 * Validates optional password change fields.
 *
 * @param {string} password - New password.
 * @param {string} passwordCheck - New password confirmation.
 * @returns {boolean} `true` when passwords are valid or both empty.
 */
function isValidPasswordChange(password, passwordCheck) {
    if (!password && !passwordCheck) {
        return true;
    }

    if (!password || !passwordCheck) {
        showValidationError("Senha incompleta", "Preencha a nova senha e a confirmação.");
        return false;
    }

    if (password !== passwordCheck) {
        showValidationError("Senhas diferentes", "As senhas devem ser iguais.");
        return false;
    }

    if (password.length < 6) {
        showValidationError("Senha muito pequena", "A senha deve ter 6 ou mais caracteres.");
        return false;
    }

    if (password.length >= 250) {
        showValidationError("Senha muito grande", "A senha deve ter menos de 250 caracteres.");
        return false;
    }

    return true;
}


/**
 * Converts all form values to trimmed strings.
 *
 * @param {Record<string, FormDataEntryValue>} data - Raw form data.
 * @returns {Record<string, string>} Normalized form data.
 */
function normalizeFormData(data) {
    return Object.fromEntries(
        Object.entries(data).map(([key, value]) => [key, String(value || "").trim()])
    );
}


/**
 * Displays a SweetAlert2 validation error.
 *
 * @param {string} title - Alert title.
 * @param {string} text - Alert message.
 * @returns {void}
 */
function showValidationError(title, text) {
    Swal.fire({
        icon: "error",
        title,
        text,
        confirmButtonText: "Tentar novamente",
    });
}


function isLettersAndSpaces(value) {
    return /^[\p{L}\s]+$/u.test(value);
}


function isLettersNumbersAndSpaces(value) {
    return /^[\p{L}\p{N}\s]+$/u.test(value);
}


function isDigits(value) {
    return /^\d+$/.test(value);
}


function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}


