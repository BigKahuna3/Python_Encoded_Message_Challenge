import requests
from html.parser import HTMLParser

coordsTable = []

class DocParser(HTMLParser):
    def __init__(self):
        super().__init__()  # initialize parent class
        self.inTable = 0
        self.inCell = 0
        self.tableRowArray = []
        
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.inTable += 1
        if tag == "td":
            self.inCell += 1

    def handle_endtag(self, tag):
        if tag == "table" :
            self.inTable -= 1
        if tag == "td":
            self.inCell -= 1
        if tag == "tr":
            # append to coordsTable when we hit the end of the row
            coordsTable.append(self.tableRowArray)
            self.tableRowArray = []

    def handle_data(self, data):
        # only record data if we are currently in a cell
        if self.inTable > 0 and self.inCell > 0:
            self.tableRowArray.append(data)

def read_doc(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP Error {e.response.status_code}: {str(e)}")
    
def get_biggest_xy_coordinate(xory):
    biggestNumber = 0
    column = 0 # default to x
    if xory == "y":
        column = 2
    for row in coordsTable:
        if row[column].isdigit():
            if int(row[column]) > biggestNumber:
                biggestNumber = int(row[column])
    return biggestNumber + 1
                    
if __name__ == "__main__":
    # Example usage
    example_url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
    
    try:
        parser = DocParser()
        content = read_doc(example_url)
        parser.feed(content)
        xBiggestNumber = get_biggest_xy_coordinate("x")
        yBiggestNumber = get_biggest_xy_coordinate("y")
        for y in range(yBiggestNumber,0,-1):
            for x in range(xBiggestNumber):
                for row in coordsTable:
                    if row[0].isdigit() and row[2].isdigit():
                        if int(row[0])==x and int(row[2])==y:
                            print(f"{row[1]}", end="")
            print("")
                
    except Exception as e:
        print(f"Error: {e}")
