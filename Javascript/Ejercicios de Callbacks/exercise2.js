const fs = require("fs");

fs.readFile("file1.txt", "utf8", (error, data1) => {

    if (error) {
        console.log("Error reading file1.txt");
        return;
    }

    fs.readFile("file2.txt", "utf8", (error, data2) => {

        if (error) {
            console.log("Error reading file2.txt");
            return;
        }

        const words1 = data1.split(/\r?\n/);
        const words2 = data2.split(/\r?\n/);

        const repeatedWords = words1.filter(word =>
            words2.includes(word)
        );

        console.log("Hidden message:");
        console.log(repeatedWords.join(" "));
    });
});