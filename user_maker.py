#!/usr/bin/env python3

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import csv


session = HTMLSession()


def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action")
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["method"] = method
    details["inputs"] = inputs
    details["action"] = action
    return details

def make_user(user):

    url = "http://db.cse.nd.edu:5000/signup/worker"
    # get all form tags
    first_form = get_all_forms(url)[0]
    form_details = get_form_details(first_form)
    data = {}
    for input_tag in form_details["inputs"]:
        if input_tag["type"] == "hidden":
            # if it's hidden, use the default value
            data[input_tag["name"]] = input_tag["value"]
            

    data["email"] = str(user[0])
    data["first_name"] = str(user[1])
    data["last_name"] = str(user[2])
    data["phone"] = str(user[3])
    data["field"] = str(user[4])
    data["password1"] = str(user[5])
    data["password2"] = str(user[5])

    url = urljoin(url, form_details["action"])

    if form_details["method"] == "post":
        res = session.post(url, data=data)
    elif form_details["method"] == "get":
        res = session.get(url, params=data)

    print("Signed up " + user[0])


def main():
    with open('Users.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            make_user(row)



if __name__ == '__main__':
    main()
# vim: set sts=4 sw=4 ts=8 expandtab ft=python: