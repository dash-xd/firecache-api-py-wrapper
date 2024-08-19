Firecache.set_credentials(
  base_api_url=BASE_API_URL,
  roblox_player_id=ROBLOX_PLAYER_ID,
  api_key=API_KEY
)

responses = []  # Initialize a list to collect the responses

# Get a document
doc, status = Firecache.Document.get(document_path="tmp/junk")
responses.append({"action": "get_document", "response": doc, "status_code": status})

# Replace a document
response, status = Firecache.Document.replace(
  document_path="tmp/junk",
  data={"mymessage": "i set the document id to 'junk' manually that's why it's not a random string"}
)
responses.append({"action": "replace_document", "response": response, "status_code": status})

# Create a document in a collection
response, status = Firecache.Document.create(
  collection_path="tmp",
  data={"mynewkey": "mynewvalue"}
)
responses.append({"action": "create_document", "response": response, "status_code": status})

response, status = Firecache.Document.replace(
  document_path="tmp/junk",
  data={"mymessage": "this 'junk' document path also contains a subcollection, use the collections api to check"}
)
responses.append({"action": "replace_document", "response": response, "status_code": status})


# Delete a document 
# response, status = Firecache.Document.delete(document_path="example/path/to/document")
# responses.append({"action": "delete_document", "response": response, "status_code": status})

# Get documents in a collection
docs, status = Firecache.Documents.get(collection_path="tmp")
responses.append({"action": "get_documents", "response": docs, "status_code": status})

# Get subcollections
subcollections, status = Firecache.Collections.get(document_path="")
responses.append({"action": "get_subcollections", "response": subcollections, "status_code": status})
