import requests

res = requests.post("http://localhost:8000/ask", json={
    "url": "https://www.amazon.in/dp/B0DW478NDF",
    "query": "Tell me about the battery"
})
print(res.json())
