const API_URL = "https://api.restful-api.dev/objects";

// Create a new user
async function createUser(user) {
    try {
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

    } catch (error) {
        throw error;
    }
}


// Get a user by ID
async function getUser(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);

        if (!response.ok) {
            throw new Error("User not found.");
        }

        return await response.json();

    } catch (error) {
        throw error;
    }
}


// Update the user's password
async function updatePassword(id, newPassword) {
    try {
        // Get the current user data
        const currentUser = await getUser(id);

        // Keep all existing data and update only the password
        const updatedData = {
            ...currentUser.data,
            password: newPassword
        };

        const response = await fetch(`${API_URL}/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                data: updatedData
            })
        });

        if (!response.ok) {
            throw new Error("Failed to update the password.");
        }

        return await response.json();

    } catch (error) {
        throw error;
    }
}


// Save the user's session
function saveSession(user) {
    localStorage.setItem("userId", user.id);
}


// Get the current user's session
function getSession() {
    return localStorage.getItem("userId");
}


// Log out the current user
function logout() {
    localStorage.removeItem("userId");
}