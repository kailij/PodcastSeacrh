import xml.etree.ElementTree as ET

# read all the xml files and store record elements in a list
def get_docs():
    files = ["./cfc-xml/cf74.xml", "./cfc-xml/cf75.xml", "./cfc-xml/cf76.xml", "./cfc-xml/cf77.xml",
             "./cfc-xml/cf78.xml", "./cfc-xml/cf79.xml"]
    res = []
    for file in files:
        with open(file) as f:
            tree = ET.parse(f)
            records = tree.getroot()
            for record in records:
                res.append(record)
    return res


# parse a tree element to json with fields: ["RECORDNUM", 'AUTHORS', 'MAJORSUBJ', "MINORSUBJ", 'ABSTRACT', 'TITLE', 'EXTRACT', 'SOURCE']
def parse_json(elem):
    # get id field information
    record_id = "00000"
    if elem.find('RECORDNUM') != -1 and elem.find('RECORDNUM') is not None and elem.find('RECORDNUM').text is not None:
        record_id = elem.find('RECORDNUM').text

    # get title field information
    title = ""
    if elem.find('TITLE') != -1 and elem.find('TITLE') is not None and elem.find('TITLE').text is not None:
        title = elem.find('TITLE').text

    # get abstract field information
    abstract = ""
    if elem.find('ABSTRACT') != -1 and elem.find('ABSTRACT') is not None and elem.find('ABSTRACT').text is not None:
        abstract = elem.find('ABSTRACT').text

    # get extract field information
    extract = ""
    if elem.find('EXTRACT') != -1 and elem.find('EXTRACT') is not None and elem.find('EXTRACT').text is not None:
        extract = elem.find('EXTRACT').text

    # get source field information
    source = ""
    if elem.find('SOURCE') != -1 and elem.find('SOURCE') is not None and elem.find('SOURCE').text is not None:
        source = elem.find('SOURCE').text

    # get authors field information
    authors = ""
    authors_elem = elem.find('AUTHORS')
    if authors_elem != -1 and authors_elem is not None:
        for author in authors_elem:
            if author is not None and author.text is not None:
                authors = authors + " " + author.text

    # get major_subjs field information
    major_subjs = ""
    major_subj_elem = elem.find('MAJORSUBJ')
    if major_subj_elem != -1 and major_subj_elem is not None:
        for major_subj in major_subj_elem:
            if major_subj is not None and major_subj.text is not None:
                major_subjs = major_subjs + " " + major_subj.text


    # get minor_subjs field information
    minor_subjs = ""
    minor_subj_elem = elem.find('MINORSUBJ')
    if minor_subj_elem != -1 and minor_subj_elem is not None:
        for minor_subj in minor_subj_elem:
            if minor_subj is not None and minor_subj.text is not None:
                minor_subjs = minor_subjs + " " + minor_subj.text




    res = {
        "RECORDNUM": record_id,
        "AUTHORS": authors,
        "TITLE": title,
        "MAJORSUBJ": major_subjs,
        "MINORSUBJ": minor_subjs,
        "ABSTRACT": abstract,
        "EXTRACT": extract,
        "SOURCE": source
    }
    return res

