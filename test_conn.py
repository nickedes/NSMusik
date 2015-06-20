import pycps


def getcon():
    # Create a connection to a Clusterpoint database.
    con = pycps.Connection('tcp://cloud-eu-0.clusterpoint.com:9007',
                           'songs', 'nkmittal4994@gmail.com', 'cluster', '1133')
    return con


def getid(con):
    results = con.retrieve_last(docs=0)
    try:
        last = results.get_documents()
        return max([int(ide) for ide in last])
    except:
        return 0

def insert(data):
    try:
        con = getcon()
        ide = getid(con)+1
        con.insert({ide: data})
    except pycps.APIError as e:
        return e
    return True
