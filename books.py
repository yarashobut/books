import requests

query = "harry potter"
url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

# we dont need api key unless we have speciifc 
#things we wanna do w the api so this is just here for 
#later if need be:
# url += f"&key={API_KEY}"

response = requests.get(url)
data = response.json()

# Print the first book title
print(data["items"][0]["volumeInfo"]["title"])
