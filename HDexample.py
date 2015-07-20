# -*- coding: cp1252 -*-
###############################################################################
#             High Dimensionality problem example                     
# Authors:
#  2015 Jose Javier Garcia Aranda , Juan Ramos Diaz
#
###############################################################################
# This High Dimensionality example creates N items (which are "users").
# Each user is defined by his profile. 
# A profile is a tuple of 10 pairs of keyword and weight ( 20 fields in total)
# weights are floating numbers and belong to 0..1
# The summation of weights of a profile is normalized to 1
# we consider 1000 diferent keywords
# A profile takes 8 keywords from first 200 keywords (the "popular" keywords)
# Each keyword is a dimension. Therefore there are 1000 possible dimensions
# A single user only have 10 dimensions
# Different users can have different dimensions.
# A new distance and equality function are defined for this use case
#
#     cl = KMeansClustering(users,HDdistItems,HDequals);
#
# Additionally, now the number of iterations can be limited in order to save time
# Experimentally, we have concluded that 10 iterations is  enough accurate for most cases.
# The new HDgetClusters() function is linear. Avoid the recalculation of centroids
# whereas original function getClusters() is N*N complex, because recalculate the
# centroid when move an item from one cluster to another. 
# This new function can be used for low and high dimensionality problems, increasing 
# performance in both cases
#
# solution = cl.HDgetclusters(numclusters,max_iterations);
#
# Other new available optimization inside HDcentroid() function in is the use of mean instead median at centroid calculation.
# median is more accurate but involves more computations when N is huge. 
# The function HDcentroid() is invoked internally by HDgetclusters()
#
# The optional invocation of HDcomputeSSE() assist the computation of the optimal number or clusters.
#
#
from cluster import KMeansClustering
from cluster import ClusteringError
from cluster import util
from cluster.util import HDcentroid
from cluster.HDdistances import HDdistItems, HDequals, HDcomputeSSE
import time
import datetime

import random

def createProfile():
    num_words=1000
    total_weight=0;
    marked_word=[0]*num_words
    repeated_word=False
    list_profile=[]    
    returned_profile=();
    profile_aux=[];
    #10 pairs word, weight.
    #Don't repeated words.
    for i in range(8):
        partial_weight=random.uniform(0,1)
        total_weight+=partial_weight
        repeated_word=False
        while repeated_word==False:
            random_word=random.randint(0,299)
            if marked_word[random_word]==0:
                marked_word[random_word]=1
                repeated_word=True
        random_word= str(random_word)
        tupla=[random_word,partial_weight]
        list_profile.append(tupla)
    for i in range(2):
        partial_weight=random.uniform(0,1)
        total_weight+=partial_weight
        repeated_word=False
        while repeated_word==False:
            random_word=random.randint(300,999)
            if marked_word[random_word]==0:
                marked_word[random_word]=1
                repeated_word=True
        random_word= str(random_word)
        tupla=[random_word,partial_weight]
        list_profile.append(tupla)
    #Normalization of the profile
    for i in range(5):
        a=list_profile[i][0]
        b=list_profile[i][1]
        b=b/total_weight; #the sum of the weights must be 1       
        profile_aux=([a,b])
        returned_profile+=tuple(profile_aux)
    return returned_profile

####################################################
#                    MAIN                          #
####################################################
sses=[0]*10 #stores the sse metric for each number of clusters from 5 to 50
num_users=100
numsse=0
numclusters=5 # starts at 5
max_iteraciones=10
ts = time.time()
start_time=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
while numclusters<=50: # compute SSE from num_clusters=5 to 50
    supersol=0#supersolucion, distancias entre el clusters y los usuarios.
    users=[] # users are the items of this example
    for i in range(num_users):#en el range el numero de usuarios
        user = createProfile()
        users.append(user)
    #x=0;
    print " inicializing kmeans..."
    cl = KMeansClustering(users,HDdistItems,HDequals);
    print " executing...",numclusters
    ts = time.time()
    st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st
    numclusters=numclusters
    solution = cl.HDgetclusters(numclusters,max_iteraciones);
    for i in range(numclusters):
        a = solution[i]
        print util.HDcentroid(a),","
    ts = time.time()
    st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    sses[numsse]=HDcomputeSSE(solution,numclusters) 
    numsse+=1
    numclusters+=5
ts = time.time()
end_time=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print "start_time:",start_time
print "end_time:",end_time
print "sses:",sses

