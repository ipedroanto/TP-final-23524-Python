console.log(location.search); // Lee los argumentos pasados a este formulario
var id = location.search.substr(4);
console.log(id);

const { createApp } = Vue;

createApp({
    data() {
        return {
            id: 0,
            nombre: "",
            apellido: "",
            email: "",
            tema: "",
            fecha_alta: "",
            url: 'http://localhost:5000/oradores/' + id,
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.id = data.id;
                    this.nombre = data.nombre;
                    this.apellido = data.apellido;
                    this.email = data.email;
                    this.tema = data.tema;
                    this.fecha_alta = data.fecha_alta;
                })
                .catch(err => {
                    console.error(err);
                    this.error = true;
                });
        },
        modificar() {
            let orador = {
                nombre: this.nombre,
                apellido: this.apellido,
                email: this.email,
                tema: this.tema,
                fecha_alta: this.fecha_alta,
            };
            var options = {
                body: JSON.stringify(orador),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            };
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado");
                    window.location.href = "./index.html";
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar");
                });
        }
    },
    created() {
        this.fetchData(this.url);
    },
}).mount('#app');