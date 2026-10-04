// Exercise 1
async function getUser() {
    const response = await fetch("https://reqres.in/api/users/2");

    const user = await response.json();

    console.log(user);
}

getUser();


// Exercise 2
async function getMissingUser() {
    try {
        const response = await fetch("https://reqres.in/api/users/23");

        if (!response.ok) {
            throw new Error("User not found");
        }

        const user = await response.json();

        console.log(user);

    } catch (error) {
        console.error(error.message);
    }
}

getMissingUser();