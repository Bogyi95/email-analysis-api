from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

emails = [
    "Please pay the invoice by tomorrow",
    "Let's schedule a meeting for Monday",
    "Huge discount on our new product",
    "Payment reminder for your subscription",
    "Team meeting about the project",
    "Special marketing offer for you"
]

labels = [
    "finance",
    "work",
    "marketing",
    "finance",
    "work",
    "marketing"
]

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(emails)

model = MultinomialNB()
model.fit(X, labels)

def classify_email_ml(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)
    return prediction[0]