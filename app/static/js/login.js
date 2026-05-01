console.log('Login script loaded.');


async function submitForm() {
    event.preventDefault(); // Evita o envio tradicional do formulário
    console.log('Form submission intercepted.');
    const form = document.getElementById('login-form');

    console.log('Form element:', form.usuario.value, form.senha.value);

    Swal.fire({
        title: 'Sucesso!',
        text: 'Sua alteração foi salva.',
        icon: 'success',
        confirmButtonText: 'Ok'
    });
}