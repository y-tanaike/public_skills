const books = ["Fiction", "Essays", "Technical books"];
console.log(books.map((book, index) => `${index + 1}: ${book}`).join("\n"));
