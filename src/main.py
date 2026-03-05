import json
from formatter import DBASOPFormatter
from bs4 import BeautifulSoup

# Load Tika JSON
with open("../tika_output.json") as f:
    data = json.load(f)

tika_doc = data[0]

# Extract text from Tika HTML
html_content = tika_doc.get("X-TIKA:content", "")

soup = BeautifulSoup(html_content, "html.parser")
text_content = soup.get_text("\n")

# Replace content with cleaned text
tika_doc["content"] = text_content

formatter = DBASOPFormatter("../sample.pdf")

chunks = formatter.chunk(tika_doc)

print("Chunks:", len(chunks))
print(json.dumps(chunks, indent=2))
