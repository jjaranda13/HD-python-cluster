
""" This file provides functionalities for High dimensionality problems but also for low dimensionality problems

    added functionalities:
    - New Distance computation
    - SSE metric computation for assist the computation of the optimal number of clusters

 Authors:
 Jose Javier Garcia Aranda
 Juan Ramos Diaz
"""
import util
import time
import datetime
import random

HD_profile_dimensions=10 #dimensions per profile, default value is 10

def HDdistItems(profile1,profile2):
    """Distance function, this distance between two profiles is defined as:
    For each keyword of user A, if the keyword is not  present in user B , then the distance for this keyword is the weight in the user A.
    If the keyword exists in both users, the weights are compared and the distance is the absolute difference.
    For each keyword present in the union of keywords of both profiles, the distance is computed and added to the total distance between both users
    """

    len1=len(profile1)/2 # len(profile1) is always pair because each dimension has a weight
    len2=len(profile2)/2 # len(profile2) is always pair because each dimension has a weight
    total_len=len1+len2 #this value usually is 20
    #factor_len=20.0/total_len #this only work if the profile has less than 10 keys
    factor_len=2.0*HD_profile_dimensions/total_len #this only work if the profile has less than 10 keys
    distance = 0.0
    marked=[0]*(total_len*2);
    for i in range(len1):
        found=False
        for j in range(len2):
            if profile1[i*2]==profile2[j*2]:
                distance+=abs(profile1[i*2+1]-profile2[j*2+1]);
                found=True;
                marked[j*2]=1;
                break;
        if found==False:
            distance+=profile1[i*2+1];

    for i in range(len2):
        if marked[i*2]==1:
            continue;
        distance+=profile2[i*2+1]
        
    distance=distance*factor_len
    return distance

def HDequals(profile1,profile2):
    for i in range(HD_profile_dimensions):
        for j in range(HD_profile_dimensions):
            if profile1[i*2]!=profile2[j*2]:
                return False
            elif profile1[i*2+1]!=profile2[j*2+1]:
                return False
            return True
    

def HDcomputeSSE(solution,numclusters):
    """This metric measure the cohesion of users into a cluster and the separation among clusters at the same time"""

    partial_solution=0
    total_solution=0
    dist=0
    for i in range(numclusters):
        partial_solution=0
        for j in solution[i]:
            dist=HDdistItems(util.HDcentroid(solution[i]),j)
            partial_solution+=dist*dist
            total_solution+=partial_solution
    return total_solution
