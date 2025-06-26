import requests
import pandas as pd
import sqlalchemy as db

#query google books AP w/ 'harry potter' 
query = "harry potter"
url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
response = requests.get(url)
books = response.json()
# we dont need api key unless we have speciifc 
#things we wanna do w the api so this is just here for 
#later if need be:
# url += f"&key={API_KEY}"

#extract relevant book data from API response
book_items = books.get("items", [])
cleaned_books = []

#extract relevant info 
for item in book_items:
  volume_info = item.get("volumeInfo", {}) #api name for book info..
  cleaned_books.append({
      "title": volume_info.get("title"),
      # join list of authors into string:
      "authors": ", ".join(volume_info.get("authors", [])), 
      "publishedDate": volume_info.get("publishedDate"),
      "publisher": volume_info.get("publisher"),
      # keep description length under TEXT size:
      "description": volume_info.get("description", "")[:255],
      "pageCount": volume_info.get("pageCount"),
      "categories": ", ".join(volume_info.get("categories", [])), # make str
      "averageRating": volume_info.get("averageRating"),
      "ratingsCount": volume_info.get("ratingsCount"),
      "language": volume_info.get("language")
  })

#load cleaned data into dataframe
df = pd.DataFrame(cleaned_books)

engine = db.create_engine('sqlite:///books.db')
df.to_sql('books', con=engine, if_exists='replace', index=False)

#display data to make sure it was saved
with engine.connect() as connection:
  query_result = connection.execute(db.text("SELECT * FROM books;")).fetchall()
  print(pd.DataFrame(query_result))