const axios = require("axios");

const API_URL = "https://api.restful-api.dev/objects";

// Exercise 1: Get all objects with data
async function getAllObjects() {
    try {
        const response = await axios.get(API_URL);

        const objects = response.data;

        const objectsWithData = objects.filter(object => object.data);

        console.log("Objects with data:");

        objectsWithData.forEach(object => {
            console.log(`
ID: ${object.id}
Name: ${object.name}
Data:`, object.data);
        });

        return objectsWithData;

    } catch (error) {
        console.error("Error:", error.message);
    }
}


// Exercise 2: Create a new sports item
async function createSportsItem(item) {
    try {
        const response = await axios.post(API_URL, {
            name: item.name,
            data: item.data
        });

        console.log("Sports item created successfully:");
        console.log(response.data);

        return response.data;

    } catch (error) {
        console.error("Error:", error.message);
    }
}


// Exercise 3: Get an object by ID
async function getObjectById(id) {
    try {
        const response = await axios.get(`${API_URL}/${id}`);

        console.log("Object found:");
        console.log(response.data);

        return response.data;

    } catch (error) {
        console.error("Error:", error.message);
    }
}


// Exercise 4: Update an object
async function updateObject(id, newData) {
    try {
        const response = await axios.put(`${API_URL}/${id}`, {
            data: newData
        });

        console.log("Object updated successfully:");
        console.log(response.data);

        return response.data;

    } catch (error) {
        console.error("Error:", error.message);
    }
}


// Testing Exercise 1
getAllObjects();

// Testing Exercise 2
// createSportsItem({
//     name: "Tennis Racket",
//     data: {
//         brand: "Wilson",
//         category: "Tennis",
//         price: 3500,
//         weight: "300g",
//         material: "Graphite"
//     }
// });

// Testing Exercise 3
getObjectById("ff808181a09d98f701a10f65d5820483");

// Testing Exercise 4
updateObject("ff808181a09d98f701a10f65d5820483", {
    brand: "Wilson",
    category: "Tennis",
    price: 4000,
    weight: "310g",
    material: "Carbon Fiber"
});