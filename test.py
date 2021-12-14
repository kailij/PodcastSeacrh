from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

es = Elasticsearch()
res = es.cat.count("podcast-index", params={"format": "json"})
print(res)
