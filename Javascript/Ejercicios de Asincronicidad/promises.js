// Exercise 1 - Promise.all()

const pokemon1 = fetch("https://pokeapi.co/api/v2/pokemon/1")
    .then(response => response.json());

const pokemon2 = fetch("https://pokeapi.co/api/v2/pokemon/4")
    .then(response => response.json());

const pokemon3 = fetch("https://pokeapi.co/api/v2/pokemon/7")
    .then(response => response.json());

Promise.all([pokemon1, pokemon2, pokemon3])
    .then(pokemons => {
        pokemons.forEach(pokemon => {
            console.log(pokemon.name);
        });
    })
    .catch(error => {
        console.error(error);
    });


// Exercise 2 - Promise.any()

const pokemon4 = fetch("https://pokeapi.co/api/v2/pokemon/1")
    .then(response => response.json());

const pokemon5 = fetch("https://pokeapi.co/api/v2/pokemon/4")
    .then(response => response.json());

const pokemon6 = fetch("https://pokeapi.co/api/v2/pokemon/7")
    .then(response => response.json());

Promise.any([pokemon4, pokemon5, pokemon6])
    .then(pokemon => {
        console.log(pokemon.name);
    })
    .catch(error => {
        console.error(error);
    });

// Exercise 3 - Promise.all() with setTimeout()

const word1 = new Promise(resolve => {
    setTimeout(() => resolve("very"), 1000);
});

const word2 = new Promise(resolve => {
    setTimeout(() => resolve("dogs"), 500);
});

const word3 = new Promise(resolve => {
    setTimeout(() => resolve("cute"), 1500);
});

const word4 = new Promise(resolve => {
    setTimeout(() => resolve("are"), 200);
});

Promise.all([word1, word2, word3, word4])
    .then(words => {
        const [very, dogs, cute, are] = words;

        console.log(`${dogs[0].toUpperCase()}${dogs.slice(1)} ${are} ${very} ${cute}`);
    });