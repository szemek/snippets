import boto3
import numpy as np
import matplotlib.pyplot as plt

BUCKET = "my-bucket"
PREFIX = "folder/subfolder/subsubfolder/"


# fetching data
s3 = boto3.client("s3")

timestamps = []

response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
timestamps += list(map(lambda x: x['LastModified'], response['Contents']))

while 'NextContinuationToken' in response.keys():
    print(response['NextContinuationToken'])

    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX, ContinuationToken=response['NextContinuationToken'])
    timestamps += list(map(lambda x: x['LastModified'], response['Contents']))

# transforming data
timestamps = list(map(lambda t: t.replace(tzinfo=None), timestamps))

timestamps = np.array(timestamps, dtype='datetime64[s]')

timestamps = timestamps.astype('float')

timestamps.sort()

diffs = np.diff(timestamps)

# plotting
fig, ax = plt.subplots()

ax.plot(diffs, '.')
plt.show()
