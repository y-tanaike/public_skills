const books = ["小説", "エッセイ", "技術書"];
console.log(books.map((book, index) => `${index + 1}: ${book}`).join("\n"));
