from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_es():
    if request.method == "POST" and "submit-query" in request.form:
        query = request.form['submit-query']
        genretype = request.form['genre']
        print(genretype)
        queryTerms = query.split(" ")
        es = Elasticsearch()
        fields = ["Name", 'Description', "Genre"]
        # Search all fields
        ds1 = {
            "query": {
                "function_score": {
                    "query": {
                        "multi_match": {
                            "fields": fields,
                            "query": query,
                        }
                    },
                    "script_score": {
                        "script": {
                            "inline": "_score > 0 ? _score + params['_source']['Rating'] + Math.log10(params["
                                      "'_source'][ "
                                      "'Rating_Volume'] + 1) * 10 : 0 "
                        }
                    }

                }
            }
        }

        # Search specific field:
        ds2 = {
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "multi_match": {
                                        "query": query,
                                        "fields": fields
                                    }
                                }, {
                                    "match": {"Genre": genretype}
                                }
                            ]
                        }
                    },
                    "script_score": {
                        "script": {
                            "inline": "_score > 0 ? _score + params['_source']['Rating'] + Math.log10(params["
                                      "'_source'][ "
                                      "'Rating_Volume'] + 1) * 10 : 0 "
                        }
                    }
                }
            }
        }

        if genretype == "all":
            res = es.search(index="podcast-index", body=ds1, size=8)
        else:
            res = es.search(index="podcast-index", body=ds2, size=8)
        # build data
        data = []
        if res is not None and "hits" in res and "hits" in res["hits"]:
            hits = res["hits"]["hits"]
            for result in hits:
                res = {}
                name = result["_source"]["Name"]
                genre = result["_source"]["Genre"]
                description = result["_source"]["Description"]
                if result["_source"]["Rating"] == "Not Found":
                    rating = 0
                else:
                    rating = round(float(result["_source"]["Rating"]), 2)
                if result["_source"]["Rating_Volume"] == "Not Found":
                    rating_num = 0
                else:
                    rating_num = int(result["_source"]["Rating_Volume"])
                res["Name"] = name
                res["Description"] = description
                res["Rating"] = rating
                res["Genre"] = genre
                res["Rating_Volume"] = rating_num

                data.append(res)
            return render_template("submit_query.html", queryRes=data, test=queryTerms, finishLoad=1)
        # return res
    return render_template("submit_query.html")


if __name__ == "__main__":
    app.run()
