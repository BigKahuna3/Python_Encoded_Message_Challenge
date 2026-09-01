import requests
from html.parser import HTMLParser

columnTable = []

def get_doc(url: str):
    try:
        ret = requests.get(url)
        ret.raise_for_status()
        return ret.text
                
    except requests.RequestException as e:
        print(f"Error: HTTP Result {requests.Response.status_code()}; {str(e)}")
        raise
    
class DocParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inTable = 0
        self.inCell = 0
        self.rowData = []
        
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.inTable += 1
        if tag == "td":
            self.inCell += 1
    
    def handle_endtag(self, tag):
        if tag == "table":
            self.inTable -= 1
        if tag == "td":
            self.inCell -+ 1
        if tag == "tr":
            columnTable.append(self.rowData)
            self.rowData = []
            
    def handle_data(self, data):
        if self.inTable > 0 and self.inCell > 0:
            self.rowData.append(data)

def get_biggest_xy(xory):
    axis = 0 # initialize to 'x'
    biggest_number = 0
    if xory == "y":
        axis = 2
    for row in columnTable:
        if row[axis].isdigit():
            if int(row[axis]) > biggest_number:
                biggest_number = int(row[axis])
    return biggest_number + 1
            
if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
    
    try:
        contents = get_doc(url)
        parser = DocParser()
        
        parser.feed(contents)
        x_biggest_number = get_biggest_xy("x")
        y_biggest_number = get_biggest_xy("y")
        
        for y in range(y_biggest_number,0,-1):
            for x in range(x_biggest_number):
                for row in columnTable:
                    if row[0].isdigit() and row[2].isdigit():
                        if int(row[0]) == x and int(row[2]) == y:
                            print(f"{row[1]}", end="")
            print("")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise
