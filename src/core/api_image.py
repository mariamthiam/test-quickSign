#!flask/bin/python
from upload_images import binary_to_image, get_db_collection
from flask import Flask
import pandas as pd


app = Flask(__name__)


@app.route('/image/<md5>')
def get_image_by_md5(md5):
    image = get_db_collection("image_handler").find_one({"md5": md5})
    if not image:
        raise FileNotFoundError(f"Can not found image with md5 {md5}")
    binary_to_image(image["original_image"]).show()
    return "200 ok"


@app.route('/monitoring')
def monitor_images():
    agg_status = get_db_collection("image_status").aggregate(
        [
            {
                "$group":
                    {
                        "_id": {
                            "minutes": {
                                "$dateToString": {
                                    "date": "$created_at",
                                    "format": "%Y-%m-%dT%H:%M"
                                }
                            },
                            "error_status": "$with_error"
                        },
                        "number_event": {
                            "$sum": 1
                        }
                    }
            }
        ]
    )
    df_agg_status = pd.DataFrame(list(agg_status))
    print(df_agg_status)
    df_agg_status.plot.hist()
    return "200 ok"


if __name__ == '__main__':
    app.run()
