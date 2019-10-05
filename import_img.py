from PIL import Image
from io import BytesIO
import numpy as np
import boto3
#import s3fs
import argparse


#Gets list of all images in bucket
def get_image_keys(bucket, folders=None):
    fs = s3fs.S3FileSystem(anon=False) #access bucket
    key_list=[]
    if folders!=None:
        if ',' in folders:
            folders=folders.split(',') # Separate folders into list
        else:
            folders=[folders]
        for folder in folders:
            keys=fs.ls(bucket+'/'+folder.strip()) # get list of all keys in bucket/folder
            for key in keys:
                if 'JPEG' in key: #checks to make sure key is legitimate and not folder path
                    key_list.append(key.strip(bucket)[1:])
        return key_list
    else:
        keys=fs.ls(bucket) # get list of all keys in bucket
        for key in keys:
            if 'JPEG' in key: #checks to make sure key is legitimate and not folder path
                key_list.append(key.strip(bucket)[1:])
        return key_list

#Saves urls to text file (for Local Spark)
def save_urls_to_txt(urls):
    with open('urls.txt', 'w') as filehandle:
        for url in urls:
            filehandle.write('%s\n' % url)

#Saves urls to log file on S3 (for Cluster Spark)
#def save_urls_to_log(urls):


#Imports image and returns array of image
def read_image_from_s3(bucket, key, region_name='us-west-2'):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    np array
        Image array
    """
#    s3 = boto3.resource('s3', region_name='us-west-2')
    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return np.array(im)

#Writes images back to S3 (only used for testing)
def write_image_to_s3(img_array, bucket, key, region_name='us-west-2'):
    """Write an image array into S3 bucket

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    None
    """
    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    file_stream = BytesIO()
    im = Image.fromarray(img_array)
    im.save(file_stream, format='jpeg')
    object.put(Body=file_stream.getvalue())




#Only used to test script
if __name__== '__main__':

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    # vvv maybe leave out or modify so only one image of choice is queried
    ap.add_argument("-b", "--bucket", required=True, type=str, default='vasco-imagenet-db', help="Name of S3 bucket")
    ap.add_argument("-f", "--folder", required=False, type=str, default=None, help="List of folders (in quotes and separated by commas)")
    ap.add_argument("-r", "--region_name", required=True, type=str, default='us-west-2', help="AWS Region of S3 Bucket")
    args=vars(ap.parse_args())

    key=get_image_keys(args["bucket"], args["folder"])
    read_image_from_s3(args["bucket"], key, args["region_name"])