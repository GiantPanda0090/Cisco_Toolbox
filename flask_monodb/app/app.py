from flask import Flask,render_template,request
from mongo import *
import pymongo


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    titles = insert_new_entry(1)
    entries =display_entries()

    if request.method == 'POST':
        if request.form['generate'] == 'Generate random Address Book entry':
            id=insert_new_entry(example_generator())
            result = collection.find({"$and": [{"_id": id}]})
            return render_template('index.html',entry=result)
    return render_template('index.html',entry =None,entries=entries,titles=titles)


if __name__ == '__main__':
    app.run()
