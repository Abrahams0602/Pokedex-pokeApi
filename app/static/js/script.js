function buscarPokemon(nombre){
    const input = document.getElementById('input-pokemon');

    if(input){
        input.value = nombre;
        const formulario = document.getElementById('form-busqueda');
        formulario.submit();
    }

}

/*.

buscarPokemon(nombre)
Es una función de conveniencia para mejorar la experiencia del usuario (UX).

Parámetro nombre: Recibe el nombre del Pokémon sobre el que se hizo clic en la lista de tipos.

Acción 1: Busca el elemento del formulario por su ID (input-pokemon) y le asigna el valor del nombre.

Acción 2: Busca el formulario de búsqueda principal (form-busqueda) y ejecuta el método .submit().

Resultado: Simula que el usuario escribió el nombre y presionó "Buscar", permitiendo ver la ficha técnica rápidamente. 

*/