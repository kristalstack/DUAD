// ========================================
// EXERCISE 1
// Loop through a list and print all elements
// ========================================

const fruits = ["apple", "pear", "grape", "orange"];

for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}


// ========================================
// EXERCISE 2
// Store even numbers in another list
// Solution using FOR
// ========================================

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const evenNumbers = [];

for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        evenNumbers.push(numbers[i]);
    }
}

console.log("Even numbers using for:", evenNumbers);


// ========================================
// EXERCISE 2
// Solution using FILTER
// ========================================

const evenNumbersFilter = numbers.filter(function(number) {
    return number % 2 === 0;
});

console.log("Even numbers using filter:", evenNumbersFilter);

// ========================================
// EXERCISE 3
// Convert Celsius temperatures to Fahrenheit using MAP
// ========================================

const celsiusTemperatures = [0, 10, 20, 30, 40];

const fahrenheitTemperatures = celsiusTemperatures.map(function(celsius) {
    return (celsius * 9 / 5) + 32;
});

console.log("Fahrenheit temperatures:", fahrenheitTemperatures);


// ========================================
// EXERCISE 4
// Convert a string into a list of words
// without using SPLIT
// ========================================

const example = "This is a simple example";

const words = [];
let currentWord = "";

for (let i = 0; i < example.length; i++) {
    if (example[i] === " ") {
        if (currentWord !== "") {
            words.push(currentWord);
            currentWord = "";
        }
    } else {
        currentWord += example[i];
    }
}

// Add the last word because there is no space after it
if (currentWord !== "") {
    words.push(currentWord);
}

console.log("Words:", words);

// ========================================
// EXERCISE 5
// Get student information and grade statistics
// ========================================

const student = {
    name: "John Doe",
    grades: [
        { name: "math", grade: 80 },
        { name: "science", grade: 95 },
        { name: "history", grade: 70 },
        { name: "PE", grade: 90 },
        { name: "music", grade: 93 }
    ]
};

let total = 0;
let highest = student.grades[0];
let lowest = student.grades[0];

for (let i = 0; i < student.grades.length; i++) {
    total += student.grades[i].grade;

    if (student.grades[i].grade > highest.grade) {
        highest = student.grades[i];
    }

    if (student.grades[i].grade < lowest.grade) {
        lowest = student.grades[i];
    }
}

const average = total / student.grades.length;

const result = {
    name: student.name,
    gradeAvg: average,
    highestGrade: highest.name,
    lowestGrade: lowest.name
};

console.log("Student result:", result);