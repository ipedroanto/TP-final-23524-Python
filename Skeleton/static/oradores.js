const { createApp } = Vue;

createApp({
    data() {
        return {
            oradores: [],
            url: 'http://127.0.0.1:5000/oradores',
            error: false,
            cargando: true,
            id: 0,
            nombre: '',
            apellido: '',
            email: '',
            tema: '',
            fecha_alta: '',
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.oradores = data;
                    this.cargando = false;
                })
                .catch(err => {
                    console.error(err);
                    this.error = true;
                });
        },
        eliminar(orador) {
            const url = this.url + '/' + orador;
            var options = {
                method: 'DELETE',
            };
            fetch(url, options)
                .then(response => response.json())
                .then(response => {
                    location.reload();
                })
        },
        grabar(){
            let orador = {
                nombre: this.nombre,
                apellido : this.apellido,
                email: this.email,
                tema : this.tema,
                fecha_alta: this.fecha_alta,
            };
            var options = {
                method: 'POST',
                body: JSON.stringify(orador),
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            };
            fetch(this.url, options)
            .then(function () {
                alert('Se registro el orador');
                window.location.href = './index.html';
            })
            .catch(err => {
                console.error(err);
            });
        }
    },
    
    created() {
        this.fetchData(this.url)
    }


}).mount('#app');