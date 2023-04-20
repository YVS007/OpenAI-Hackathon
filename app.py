from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import json
from api import *

app = Flask(__name__)


def tagsplit(tagstring_list):
    tag_list=[]
    for tagstring in tagstring_list:
        tag_list.append(tagstring.split(","))
    return tag_list

@app.route('/get_tickets_with_tag', methods=['GET'])
def get_tickets_with_tag():
    tag = request.args.get('tag')
    data = read_ticket_data()
    tickets_with_tag = []
    for i in range(len(data['tags'])):
        if tag in data['tags'][i]:
            tickets_with_tag.append({
                'ticketid': data['ticketid'][i],
                'ticket': data['ticket'][i],
                'tags': data['tags'][i]
            })
    return jsonify({'tickets': tickets_with_tag})


@app.route('/',methods=['POST','GET'])
def index():
    tag_for_modal = request.args.get('tag')
    data = pd.read_csv('data.csv')
    # ticket_data = data['ticket'][ticket_id]
    # resolution = inference_on_model(ticket_data,FINE_TUNED_MODEL)
    data['tags'] = tagsplit(list(data['tags']))  #splitting tag strings to a list
    data = data.to_dict('dict')
    return render_template('techniciandashboard.html', data=data,tag_for_modal=tag_for_modal)


@app.route('/ticketdetails/<int:ticket_id>',methods=['POST','GET'])
def ticketdetails(ticket_id):
    data = pd.read_csv('data.csv')
    data_row = get_output_data_for_ticket(data,ticket_id)
    tag_for_modal = request.args.get('tag')
    data['tags'] = tagsplit(list(data['tags']))  #splitting tag strings to a list
    data2 = data.to_dict('dict')
    kg_data = json.loads( data_row['knowledgegraph'][0] )
    return render_template('ticketdetails.html', data_row = data_row,kg_data = kg_data, data = data2, tag_for_modal=tag_for_modal)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)