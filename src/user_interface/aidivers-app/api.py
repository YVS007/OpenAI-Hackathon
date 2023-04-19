import re
import openai
import json
import pandas as pd
import csv 

CSV_FILE = 'data.csv'
FINE_TUNED_MODEL = 'davinci:ft-personal-2023-04-12-09-28-32'

openai.api_key = "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"

def read_ticket_data():
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        tickets = []
        for row in reader:
            ticket = {"id": row[0], "description": row[1]}
            tickets.append(ticket)
        print("Tickets",tickets)    
        return tickets


def extract_resolution_from_response(response):
    text = response.choices[0].text
    resolution_array = text.split("[END]")
    if len(resolution_array) >= 3:
        resolution = "1st resolution:" + resolution_array[0] + "\n" + "2nd resolution:" + resolution_array[1] + "\n" + "3rd resolution" + resolution_array[2]
    else: 
        resolution = text
    return resolution

def get_resolution_of_ticket(prompt,FINE_TUNED_MODEL):
    response = openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt=prompt,
    temperature=0.7,
    max_tokens=400,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=1 )
    print("resp1",response)
    resolution = extract_resolution_from_response(response)
    return resolution

def get_output_data_for_ticket(data,ticket_id):
    print("Inside_putput")
    data_row = data[ data['ticketid'] == ticket_id].reset_index(drop=True)
    prompt = data_row['ticket'][0]
    print("prompt",prompt)
    data_row['resolution'] = get_resolution_of_ticket(prompt,FINE_TUNED_MODEL)
    print("resolution",data_row['resolution'] )
    data_row['rootcause'] = data_row['rootcause']

    return data_row
    
    

