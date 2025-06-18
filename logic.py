import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from database.models import Product

# Initialize NLTK tools
nltk.download('punkt')
nltk.download('stopwords')
ps = PorterStemmer()

def preprocess_text(message):
    # Tokenize the message
    words = word_tokenize(message.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    # Apply stemming
    stemmed_words = [ps.stem(word) for word in filtered_words]
    
    return stemmed_words

def get_book_suggestions(message):
    # Preprocess the message
    processed_message = preprocess_text(message)
    
    # If there's no useful keyword after preprocessing
    if not processed_message:
        return "Sorry, I couldn't understand your request. Could you please clarify?"

    # Example: Use processed keywords to search the database
    query = " ".join(processed_message)  # Join back into a string for database search

    books = Product.query.filter(Product.name.ilike(f'%{query}%')).limit(5).all()

    if books:
        suggestions = []
        for book in books:
            suggestions.append(f"{book.name} - Rs. {book.price}\n{book.description}")
        return "\n\n".join(suggestions)
    else:
        return "Sorry, no books found matching that request."