
window.addEventListener("load", function () {
    const formulario = document.getElementById('formulario');
    const formulariol = document.getElementById('formulariol');

    const inputs = document.querySelectorAll('#formulario input');

    const expresiones = {
        name: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
        last: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
        username: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
        password: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/, // 8 o más caracteres, mayuscula.
        email: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    }

    const campos = {
        name: false,
        last: false,
        username: false,
        password: false,
        email: false
    }

    const validarFormulario = (e) => {
        switch (e.target.name) {
            case "name":
                validarCampo(expresiones.name, e.target, 'name');
                break;
            case "last":
                validarCampo(expresiones.last, e.target, 'last');
                break;
            case "username":
                validarCampo(expresiones.username, e.target, 'username');
                break;
            case "email":
                validarCampo(expresiones.email, e.target, 'email');
                validarconfirmPassword();
                break;
            case "password":
                validarCampo(expresiones.password, e.target, 'password');
                break;
            case "confirmPassword":
                validarconfirmPassword();
                break;

        }
    }

    const validarCampo = (expresion, input, campo) => {
        if (expresion.test(input.value)) {
            document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
            document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
            document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
            campos[campo] = true;
        } else {
            document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
            document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
            document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
            campos[campo] = false;
        }
    }

    const validarconfirmPassword = () => {
        const inputPassword1 = document.getElementById('password');
        const inputconfirmPassword = document.getElementById('confirmPassword');

        if (inputPassword1.value !== inputconfirmPassword.value) {
            document.getElementById(`grupo__confirmPassword`).classList.add('formulario__grupo-incorrecto');
            document.getElementById(`grupo__confirmPassword`).classList.remove('formulario__grupo-correcto');
            document.querySelector(`#grupo__confirmPassword .formulario__input-error`).classList.add('formulario__input-error-activo');
            campos['password'] = false;
        } else {
            document.getElementById(`grupo__confirmPassword`).classList.remove('formulario__grupo-incorrecto');
            document.getElementById(`grupo__confirmPassword`).classList.add('formulario__grupo-correcto');
            document.querySelector(`#grupo__confirmPassword .formulario__input-error`).classList.remove('formulario__input-error-activo');
            campos['password'] = true;
        }
    }

    inputs.forEach((input) => {
        input.addEventListener('keyup', validarFormulario);
        input.addEventListener('blur', validarFormulario);
    });

    if (formulario) {
        formulario.addEventListener('submit', (e) => {

            const terms = document.getElementById('terms');
            if (campos.name && campos.last && campos.username && campos.email && campos.password && terms.checked) {
                formulario.submit();

            } else {
                e.preventDefault();
                document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');

                setTimeout(() => {
                    document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
                }, 5000);

            }
        });

    }

    if (formulariol) {
        formulariol.addEventListener('submit', (e) => {

            const emaill = document.getElementById('emaill').value;
            const passwordl = document.getElementById('passwordl').value;
            if (emaill != "" && passwordl != "") {
                formulario.submit();

            } else {
                e.preventDefault();
                document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');

                setTimeout(() => {
                    document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
                }, 5000);

            }
        });

    }


    $(document).ready(function () {

        //Pagina de buscar tweets

        // Ocultar todos los contenedores de contenido al cargar la página
        $("#contenido_query, #contenido_usuario, #contenido_hashtag").hide();

        // Deshabilitar el botón de envío al cargar la página
        $('#busc_tweets').attr('disabled', 'disabled');

        // Mostrar el contenido correspondiente al seleccionar una opción
        $("#opciones").change(function () {
            var seleccion = $(this).val();

            // Ocultar todos los contenedores de contenido
            $("#contenido_query, #contenido_usuario, #contenido_hashtag").hide();

            // Mostrar el contenedor correspondiente a la opción seleccionada
            $("#contenido_" + seleccion).show();

            // Verificar si se ha seleccionado una opción y si los campos de texto están vacíos
            var camposVacios = $("#contenido_" + seleccion + " input[type='text']").filter(function () {
                return $(this).val() === "";
            });

            if (seleccion === '' || camposVacios.length > 0) {
                // Deshabilitar el botón de envío
                $('button[type="submit"]').attr('disabled', 'disabled');
            } else {
                // Habilitar el botón de envío
                $('button[type="submit"]').removeAttr('disabled');
            }
        });

        // Verificar si los campos de texto están vacíos al escribir en ellos
        $("#contenido_query input[type='text'], #contenido_usuario input[type='text'], #contenido_hashtag input[type='text']").keyup(function () {
            var seleccion = $("#opciones").val();

            // Verificar si se ha seleccionado una opción y si los campos de texto están vacíos
            var camposVacios = $("#contenido_" + seleccion + " input[type='text']").filter(function () {
                return $(this).val() === "";
            });

            if (seleccion === '' || camposVacios.length > 0) {
                // Deshabilitar el botón de envío
                $('button[type="submit"]').attr('disabled', 'disabled');
            } else {
                // Habilitar el botón de envío
                $('button[type="submit"]').removeAttr('disabled');
            }
        });



        $(".filtros_btn").click(function () {

            $("#filtros").toggle("slow");
            $("#filtros").css("display", "flex");
        });

        $("#opc_an").prop("disabled", true);

        // Escuchar el evento change del campo select
        $("#tipo_sent").change(function () {
            // Obtener el valor seleccionado
            var selectedOption = $(this).val();

            // Activar o desactivar el botón de envío según la selección
            if (selectedOption !== "") {
                $("#opc_an").prop("disabled", false);
            } else {
                $("#opc_an").prop("disabled", true);
            }
        });


    });


    var closeButton = document.getElementById("cerrar_sesion_link");
    if (closeButton) {
        closeButton.addEventListener("click", function () {
            var firstLink = document.getElementById("datos_usuario_link");
            if (firstLink) {
                showContent("datos_usuario", firstLink);
            }
        });
    }

    var eliminarSeleccionadasBtn = document.getElementById('eliminarSeleccionadasBtn');
    var deleteForm = document.getElementById('deleteForm');
    if (eliminarSeleccionadasBtn && deleteForm) {
        eliminarSeleccionadasBtn.addEventListener('click', function() {
            deleteForm.submit();
        });
    }

});

function showContent(contentId, link) {
    var contents = document.getElementById("opciones_perfil").children[0].children;
    var links = document.getElementsByClassName("list-group-item");

    for (var i = 0; i < contents.length; i++) {
        if (contents[i].id === contentId) {
            contents[i].style.display = "block";
        } else {
            contents[i].style.display = "none";
        }
    }

    for (var j = 0; j < links.length; j++) {
        links[j].classList.remove("active");
    }

    link.classList.add("active");
}


function eliminarQuery(queryId) {
    // Aquí puedes agregar la lógica para eliminar el query con el ID proporcionado
    console.log("Eliminar query:", queryId);
}

function eliminarSeleccionados() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var queryIds = [];
    for (var i = 0; i < checkboxes.length; i++) {
        queryIds.push(checkboxes[i].value);
    }
    if (queryIds.length > 0) {
        // Aquí puedes agregar la lógica para eliminar los queries seleccionados
        console.log("Eliminar seleccionados:", queryIds);
    } else {
        alert("No se ha seleccionado ningún query.");
    }
}

function toggleSubmitButton(checkbox) {
    var submitContainer = document.getElementById('submitContainer');
    var checkboxes = document.querySelectorAll('input[name="query_id"]:checked');
    var selectedOptions = document.querySelectorAll('input[name="query_id"]:checked');
    var selectedOptionsText = document.getElementById('selectedOptionsText');

    selectedOptionsText.textContent = 'Opciones seleccionadas: ' + selectedOptions.length;
    if (checkboxes.length > 0) {
        submitContainer.style.display = 'block';
    } else {
        submitContainer.style.display = 'none';
    }
}

function deselectAllOptions() {
    var checkboxes = document.querySelectorAll('input[name="query_id"]');
    checkboxes.forEach(function (checkbox) {
        checkbox.checked = false;
    });

    var selectedOptionsText = document.getElementById('selectedOptionsText');
    selectedOptionsText.textContent = 'Opciones seleccionadas: 0';

    var submitContainer = document.getElementById('submitContainer');
    submitContainer.style.display = 'none';


}