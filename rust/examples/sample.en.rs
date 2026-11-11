fn main() {
    let books: [&str; 3] = ["Fiction", "Essays", "Technical books"];
    println!("{}", books.join(", "));
}
