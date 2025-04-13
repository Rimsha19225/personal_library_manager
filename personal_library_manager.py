import streamlit as st
import json

class PersonalLibraryManager:
    def __init__(self):
        self.library = []

    def add_book(self, title, author, year, genre, read):
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }
        self.library.append(book)

    def remove_book(self, title):
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]

    def search_book(self, query, search_by="title"):
        return [
            book for book in self.library
            if query.lower() in book[search_by].lower()
        ]

    def view_books(self):
        return self.library

    def get_statistics(self):
        total_books = len(self.library)
        read_books = len([book for book in self.library if book["read"]])
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        return total_books, percentage_read

    def save_library(self, filename="library.txt"):
        try:
            with open(filename, 'w') as f:
                json.dump(self.library, f)
        except Exception as e:
            st.error(f"Error saving library: {e}")

    def load_library(self, filename="library.txt"):
        try:
            with open(filename, 'r') as f:
                self.library = json.load(f)
        except FileNotFoundError:
            st.info("Library file not found. Starting with an empty library.")
        except json.JSONDecodeError:
            st.error("Error decoding JSON from library file.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# Initialize
if "library_manager" not in st.session_state:
    st.session_state.library_manager = PersonalLibraryManager()
    st.session_state.library_manager.load_library("library.txt")

# Streamlit App
st.title("📚 Personal Library Manager")
st.markdown("### Welcome to your Personal Library Manager!")

# Menu
menu = st.selectbox("Choose an option:", [
    "Add a book",
    "Remove a book",
    "Search for a book",
    "Display all books",
    "Display statistics",
    "Exit"
])

if menu == "Add a book":
    st.header("➕ Add a Book")
    title = st.text_input("Enter the book title", key="title")
    author = st.text_input("Enter the author", key="author")
    year = st.text_input("Enter the publication year", key="year")
    genre = st.text_input("Enter the genre", key="genre")
    read_status = st.radio("Have you read this book?", ("yes", "no"), key="read_status")

    read = True if read_status == "yes" else False
    if st.button("Add Book"):
        if title and author and year.isdigit() and genre:
            st.session_state.library_manager.add_book(title, author, int(year), genre, read)
            st.session_state.library_manager.save_library()
            st.success("Book added successfully!")
            read_label = "Read" if read else "Unread"
            st.markdown("#### 📗 Recently Added Book")
            st.write(f"{title} by {author} ({year}) - {genre} - {read_label}")
        else:
            st.error("Please provide valid inputs.")

elif menu == "Remove a book":
    st.header("❌ Remove a Book")
    remove_title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        st.session_state.library_manager.remove_book(remove_title)
        st.success("Book removed successfully!")

elif menu == "Search for a book":
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by", ["title", "author"])
    query = st.text_input(f"Enter the {search_by}")
    if st.button("Search"):
        results = st.session_state.library_manager.search_book(query, search_by)
        if results:
            st.subheader("Matching Books:")
            for i, book in enumerate(results, 1):
                read_status = "Read" if book["read"] else "Unread"
                st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
        else:
            st.warning("No matching books found.")

elif menu == "Display all books":
    st.header("📖 Your Library")
    books = st.session_state.library_manager.view_books()
    if books:
        for i, book in enumerate(books, 1):
            read_status = "Read" if book["read"] else "Unread"
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        st.info("Your library is empty.")

elif menu == "Display statistics":
    st.header("📊 Library Statistics")
    total, percentage = st.session_state.library_manager.get_statistics()
    st.write(f"**Total books:** {total}")
    st.write(f"**Percentage read:** {percentage:.1f}%")

elif menu == "Exit":
    st.session_state.library_manager.save_library("library.txt")
    st.success("Library saved to library.txt. Goodbye! 👋")
