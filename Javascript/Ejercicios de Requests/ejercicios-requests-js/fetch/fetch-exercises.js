const API_URL = "https://api.restful-api.dev/objects";

// Exercise 1: Get all objects with data
async function getAllObjects() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Failed to retrieve objects.");
        }

        const objects = await response.json();

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
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: item.name,
                data: item.data
            })
        });

        if (!response.ok) {
            throw new Error("Failed to create the sports item.");
        }

        const newItem = await response.json();

        console.log("Sports item created successfully:");
        console.log(newItem);

        return newItem;

    } catch (error) {
        console.error("Error:", error.message);
    }
}


// Exercise 3: Get an object by ID
async function getObjectById(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);

        if (!response.ok) {
            throw new Error("Object not found.");
        }

        const object = await response.json();

        console.log("Object found:");
        console.log(object);

        return object;

    } catch (error) {
        console.error("Error:", error.message);
    }
}


// Exercise 4: Update an object
async function updateObject(id, newData) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                data: newData
            })
        });

        if (!response.ok) {
            throw new Error("Failed to update the object.");
        }

        const updatedObject = await response.json();

        console.log("Object updated successfully:");
        console.log(updatedObject);

        return updatedObject;

    } catch (error) {
        console.error("Error:", error.message);
    }
}


// Testing Exercise 1
getAllObjects();


// Testing Exercise 2
createSportsItem({
    name: "Mountain Bike",
    data: {
        brand: "Trek",
        category: "Mountain Bike",
        price: 15000,
        color: "Black",
        size: "Medium"
    }
});

getObjectById("ff808181a09d98f701a10f5f091f0475");

updateObject("ff808181a09d98f701a10f5f091f0475", {
    brand: "Trek",
    category: "Mountain Bike",
    price: 17000,
    color: "Red",
    size: "Large"
});