import pycps

# Create a connection to a Clusterpoint database.
con = pycps.Connection('tcp://cloud-eu-0.clusterpoint.com:9007', 'songs', 'nkmittal4994@gmail.com', 'cluster', '250')

doc = {'title': 'Test', 'text': 'First text.'}
con.insert({5: doc})
