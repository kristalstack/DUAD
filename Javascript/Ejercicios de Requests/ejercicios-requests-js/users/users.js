const API_URL = "https://api.restful-api.dev/objects";


// Create a new user
async function createUser(user) {
    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: user.name,
            data: {
                name: user.name,
                email: user.email,
                password: user.password,
                age: user.age,
                city: user.city
            }
        })
    });

    if (!response.ok) {
        throw new Error("Failed to create the user.");
    }

    return await response.json();
}


// Get a user by ID
async function getUser(id) {
    const response = await fetch(`${API_URL}/${id}`);

    if (response.status === 404) {
        const error = new Error("User not found.");
        error.status = 404;
        throw error;
    }

    if (!response.ok) {
        const error = new Error("Failed to retrieve the user.");
        error.status = response.status;
        throw error;
    }

    return await response.json();
}


// Update user password
async function updatePassword(id, newPassword) {
    const response = await fetch(`${API_URL}/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            data: {
                password: newPassword
            }
        })
    });

    if (response.status === 404) {
        const error = new Error("User not found.");
        error.status = 404;
        throw error;
    }

    if (!response.ok) {
        const error = new Error("Failed to update the password.");
        error.status = response.status;
        throw error;
    }

    return await response.json();
}


// Save the logged-in user's ID
function saveSession(userId) {
    localStorage.setItem("userId", userId);
}


// Get the logged-in user's ID
function getSession() {
    return localStorage.getItem("userId");
}


// Remove the current session
function logout() {
    localStorage.removeItem("userId");
}