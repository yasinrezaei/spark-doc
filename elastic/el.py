from elasticsearch import Elasticsearch

# Connect to the local Elasticsearch instance
es = Elasticsearch("http://localhost:9200")
# Example document
doc = {
    "username": "Yasin",
}

# Indexing the document (id is optional)
res = es.index(index="test-index", id=1, document=doc)
print(res['result'])

# # Search for a document
# res = es.search(index="test-index", query={"match_all": {}})
# print("Got %d Hits:" % res['hits']['total']['value'])

# # Print search results
# for hit in res['hits']['hits']:
#     print(f"ID: {hit['_id']}, Source: {hit['_source']}")
