# from flask import Flask,request,jsonify,render_template
# import pickle
# import os

# app = Flask(__name__)

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# movies_path = os.path.join(base_dir,"movies.pkl")
# similarity_path = os.path.join(base_dir,"similarity.pkl")


# movies = pickle.load(open(movies_path,"rb"))
# similarity = pickle.load(open(similarity_path,"rb"))

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/recommend",methods=["POST"])
# def recommend():
#     try:
#         data = request.get_json()

#         if not data:
#             return jsonify({
#                 "error":"No movie data received."
#             }),400
        
#         movie = data.get("movie","").strip()

#         if not movie:
#             return jsonify({
#                 "error" : "plz enter a movie name."
#             }),400

#         print("Searching movie:",movie)
#         titles = movies["title"].astype(str).str.strip().str.lower()
#         matches= titles == movie.lower()

#         matching_indices = movies.index[
#            titles == movie.lower()
#        ]

#         if len(matching_indices) == 0:
#             matching_indices = movies.index[
#                 titles.str.contains(
#                 movie.lower(),
#                 case = False,
#                 na = False
#             )]

#         if len(matching_indices) == 0:
#             return jsonify({
#                 "error" : f'movie "{movie}" was not found!'
#             }),404

#         movie_index = matching_indices[0]
#         position = movies.index.get_loc(movie_index)

#         distances = similarity[position]

#         movie_list = sorted(
#             list(enumerate(distances)),
#             reverse=True,
#             key=lambda x:x[1]
#         )[1:6]

#         recommendations = []

#         for i,score in movie_list:
#             recommendations.append({
#             "title" : str(movies.iloc[i]["title"]),
#             "score" : round(float(score)*100,2)
#             })

#         selected_movie = str(
#             movies.loc[
#                 movie_index,
#                 "title"
#             ]
#         )
        
#         return jsonify({
#             "movie" :selected_movie,
#             "recommendations" : recommendations
#         })
#     except Exception as e:
#         print("Recommendation Error:",e)

#         return jsonify({
#             "error":
#                 f"Server Error: {str(e)}"
#         }),500

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import pickle
import os

app = Flask(__name__)


# Load model files
base_dir = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

movies_path = os.path.join(
    base_dir,
    "movies.pkl"
)

similarity_path = os.path.join(
    base_dir,
    "similarity.pkl"
)


movies = pickle.load(
    open(movies_path, "rb")
)

similarity = pickle.load(
    open(similarity_path, "rb")
)


# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Recommendation API
@app.route("/recommend", methods=["POST"])
def recommend():

    try:

        # 1. Get request data
        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No movie data received."
            }), 400


        # 2. Get movie name
        movie = data.get(
            "movie",
            ""
        ).strip()


        if not movie:

            return jsonify({
                "error": "Please enter a movie name."
            }), 400


        print("Searching movie:", movie)


        # 3. Prepare movie titles
        titles = (
            movies["title"]
            .astype(str)
            .str.strip()
            .str.lower()
        )


        # 4. Find exact movie
        matching_indices = movies.index[
            titles == movie.lower()
        ]


        # 5. If exact movie isn't found,
        #    try partial match
        if len(matching_indices) == 0:

            matching_indices = movies.index[
                titles.str.contains(
                    movie,
                    case=False,
                    na=False
                )
            ]


        # 6. Movie doesn't exist
        if len(matching_indices) == 0:

            return jsonify({
                "error":
                    f'Movie "{movie}" was not found!'
            }), 404


        # 7. Get movie index
        movie_index = matching_indices[0]


        # 8. Convert DataFrame index
        #    to similarity matrix position
        position = movies.index.get_loc(
            movie_index
        )


        # 9. Get similarity scores
        distances = similarity[position]


        # 10. Sort by similarity
        movie_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]


        # 11. Create recommendations
        recommendations = []


        for i, score in movie_list:

            recommendations.append({

                "title":
                    str(movies.iloc[i]["title"]),

                "score":
                    round(
                        float(score) * 100,
                        2
                    )

            })


        # 12. Get selected movie title
        selected_movie = str(
            movies.loc[
                movie_index,
                "title"
            ]
        )


        # 13. Send response
        return jsonify({

            "movie": selected_movie,

            "recommendations":
                recommendations

        })


    except Exception as e:

        print(
            "Recommendation Error:",
            e
        )

        return jsonify({

            "error":
                f"Server Error: {str(e)}"

        }), 500


# Run Flask
if __name__ == "__main__":

    app.run(
        debug=True
    )