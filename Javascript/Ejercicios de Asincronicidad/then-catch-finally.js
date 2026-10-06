// Exercise 1 - then(), catch(), finally()

fetch("https://reqres.in/api/users/2")
    .then(response => {
        if (!response.ok) {
            throw new Error("User not found");
        }

        return response.json();
    })
    .then(user => {
        console.log(user);
    })
    .catch(error => {
        console.error(error.message);
    })
    .finally(() => {
        console.log("Request completed");
    });


// Exercise 2 - then(), catch(), finally()

fetch("https://reqres.in/api/users/23")
    .then(response => {
        if (!response.ok) {
            throw new Error("User not found");
        }

        return response.json();
    })
    .then(user => {
        console.log(user);
    })
    .catch(error => {
        console.error(error.message);
    })
    .finally(() => {
        console.log("Request completed");
    });