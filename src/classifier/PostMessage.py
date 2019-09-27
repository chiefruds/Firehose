import requests


def postMessage(title: str, content: str, category: str):
    cid: int
    if category == "saving":
        cid = 5
    elif category == "investing":
        cid = 6
    elif category == "insurance":
        cid = 7
    elif category == "health":
        cid = 8
    elif category == "mortgage":
        cid = 9
    elif category == "loan":
        cid = 10
    elif category == "retirement":
        cid = 11
    else:
        cid = 0
    headers = {
        'Authorization': 'Bearer a5a2863c-774f-417f-a3f9-767e56f7ed82',
    }

    data = {
      'title': title,
      'content': content,
      'cid': cid
    }
    if cid != 0:
        response = requests.post('http://localhost:4567/api/v1/topics', headers=headers, data=data)
        print(response)
    return

if __name__ == "__main__":
    postMessage("@Add", "This is a question for a mortgage", "health")
