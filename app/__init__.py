# import the necessary packages
import hashing as hs
from imutils import paths
import argparse
import pickle
import vptree
import time
import json
import cv2
import os
import urllib.request
import numpy as np

#Walk through VPTree directory and unpack models
import glob
import pickle

#Flask packages
from flask import Flask, render_template, request, jsonify

# create flask instance
app = Flask(__name__)

#INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')


# main route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():

    if request.method == "POST":

        RESULTS_ARRAY = []

        # get url
        image_url = request.form.get('img')
        print(image_url)
        try:
            # download image into array (from url)
            if 'http' in image_url:
                resp = urllib.request.urlopen(image_url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            else:                
                # load the input query image (from webserver folder)
                image = cv2.imread('.'+image_url.split('..')[-1])

            # compute the hash for the query image, then convert it
            queryHash = hs.dhash(image, 32) #manually change to match indexed iumages
            queryHash = hs.convert_hash(queryHash)

            # load the VP-Tree and hashes dictionary
            print("[INFO] loading VP-Tree and hashes...")
            hashes=pickle.loads(open('static/pickles/img_hash_dictionary.pickle', "rb").read())

            start = time.time()
            resultsList=[] #Adds results of image query to this list
            for pickleTree in glob.glob("static/pickles/vptree_*.pickle"):
                #print("[INFO] loading VP-Tree: {pickle}".format(pickle=pickleTree))
                with open(pickleTree,'rb') as f:
                    tree=pickle.load(f)

                #Perform search in VPTree
                #print("[INFO] performing search on {pickle}".format(pickle=pickleTree))
                results = tree.get_all_in_range(queryHash, 50) #Tune to lower computational time but yield at least four results
                results = sorted(results)

                #Loop through reults and add to resultsList
                counter=0 #Ensure that only top 10 results are used
                for i, result in enumerate(results):
                    resultsList.append(result)
                    if i>=1:
                        break #Grabs first result (modifiable), moves on to next tree
                    else:
                        i+=1
            #Sort final list of all resutls
            resultsList=sorted(resultsList)
            end = time.time()
            print("[INFO] search took {} seconds".format(end - start))

            # loop over the results 
            for (score, h) in resultsList[:10]:
                #grab all image paths in our dataset with the same hash
                resultPaths = [hashes.get(int(h), [])]
                print("[INFO] {} total images(s) with d: {}, h:{}".format(len(resultPaths), score, h))
                # loop over the result paths
                for resultID in resultPaths:
                    #Remove URL Path Prefix (prefix is already included in output)
                    #resultID=str(resultID).split('/')[-1]                    
#                    print(resultID)
                    # load the result image and display it to our screeni
#                    RESULTS_ARRAY.append(
 #                       {"image": str(resultID), "score": str(score)})
#                    print(RESULTS_ARRAY)
                    RESULTS_ARRAY.append(
                        {"image": 'http://vasco-imagenet-db.s3-us-west-2.amazonaws.com/'+str(resultID), "score": str(score)})
                        #Change the bucket to match what is being queired and change view permissions
             # return success
            print(RESULTS_ARRAY)
            return jsonify(results=(RESULTS_ARRAY[:4]))

        except:

            # return error
            #return jsonify({"sorry": "Sorry, no results! Please try again."}), 500
            raise

# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

