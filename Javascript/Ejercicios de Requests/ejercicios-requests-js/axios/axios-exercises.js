const API_URL = "https://api.restful-api.dev/objects";


// Exercise 1: Get all objects with data
async function getAllObjects() {
    try {
        const response = await axios.get(API_URL);

        const objectsWithData = response.data.filter(object => object.data);

        console.log("Objects with data:");

        objectsWithData.forEach(object => {
            console.log(`
ID: ${object.id}
Name: ${object.name}
Data:`, object.data);
        });

        return objectsWithData;

    } catch (error) {
        if (error.response) {
            console.error(
                `Error: The server returned status ${error.response.status}.`
            );
        } else {
            console.error("Error: Could not connect to the server.");
        }
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
        if (error.response) {
            console.error(
                `Error: The server returned status ${error.response.status}.`
            );
        } else {
            console.error("Error: Could not connect to the server.");
        }
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
        if (error.response) {
            if (error.response.status === 404) {
                console.error("Error: Object not found.");
            } else {
                console.error(
                    `Error: The server returned status ${error.response.status}.`
                );
            }
        } else {
            console.error("Error: Could not connect to the server.");
        }
    }
}


// Exercise 4: Update an object
async function updateObject(id, newData) {
    try {
        const response = await axios.patch(`${API_URL}/${id}`, {
            data: newData
        });

        console.log("Object updated successfully:");
        console.log(response.data);

        return response.data;

    } catch (error) {
        if (error.response) {
            if (error.response.status === 404) {
                console.error("Error: Object not found.");
            } else {
                console.error(
                    `Error: The server returned status ${error.response.status}.`
                );
            }
        } else {
            console.error("Error: Could not connect to the server.");
        }
    }
}


// Run exercises in order
async function runExercises() {
    await getAllObjects();

    const newItem = await createSportsItem({
        name: "Tennis Racket",
        data: {
            brand: "Wilson",
            category: "Tennis",
            price: 3500,
            weight: "300g",
            material: "Graphite"
        }
    });

    if (!newItem) {
        return;
    }

    await getObjectById(newItem.id);

    await updateObject(newItem.id, {
        brand: "Wilson",
        category: "Tennis",
        price: 4000,
        weight: "310g",
        material: "Carbon Fiber"
    });
}

runExercises();