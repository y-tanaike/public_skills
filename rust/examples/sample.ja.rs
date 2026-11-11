fn main() {
    let books: [&str; 3] = ["小説", "エッセイ", "技術書"];
    println!("{}", books.join(", "));
}
