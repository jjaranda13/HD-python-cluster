DESCRIPTION
===========

.. image:: https://readthedocs.org/projects/python-cluster/badge/?version=latest
    :target: http://python-cluster.readthedocs.org
    :alt: Documentation Status

python-cluster is a "simple" package that allows to create several groups
(clusters) of objects from a list. It's meant to be flexible and able to
cluster any object. To ensure this kind of flexibility, you need not only to
supply the list of objects, but also a function that calculates the similarity
between two of those objects. For simple datatypes, like integers, this can be
as simple as a subtraction, but more complex calculations are possible. Right
now, it is possible to generate the clusters using a hierarchical clustering
and the popular K-Means algorithm. For the hierarchical algorithm there are
different "linkage" (single, complete, average and uclus) methods available.

Algorithms are based on the document found at
http://www.elet.polimi.it/upload/matteucc/Clustering/tutorial_html/

.. note::
    The above site is no longer avaialble, but you can still view it in the
    internet archive at:
    https://web.archive.org/web/20070912040206/http://home.dei.polimi.it//matteucc/Clustering/tutorial_html/


USAGE
=====

A simple python program could look like this::

   >>> from cluster import HierarchicalClustering
   >>> data = [12,34,23,32,46,96,13]
   >>> cl = HierarchicalClustering(data, lambda x,y: abs(x-y))
   >>> cl.getlevel(10)     # get clusters of items closer than 10
   [96, 46, [12, 13, 23, 34, 32]]
   >>> cl.getlevel(5)      # get clusters of items closer than 5
   [96, 46, [12, 13], 23, [34, 32]]

Note, that when you retrieve a set of clusters, it immediately starts the
clustering process, which is quite complex. If you intend to create clusters
from a large dataset, consider doing that in a separate thread.

For K-Means clustering it would look like this::

    >>> from cluster import KMeansClustering
    >>> cl = KMeansClustering([(1,1), (2,1), (5,3), ...])
    >>> clusters = cl.getclusters(2)

The parameter passed to getclusters is the count of clusters generated.


.. image:: https://readthedocs.org/projects/python-cluster/badge/?version=latest
    :target: http://python-cluster.readthedocs.org
    :alt: Documentation Status



2015/07/20 NEW FUNCTIONALITIES FOR HIGH AND LOW DIMENSIONALITY PROBLEMS
=======================================================================
Authors of new added functionalities:
  Garcia Aranda, Jose Javier	jose_javier.garcia_aranda@alcatel-lucent.com
  Ramos Diaz, Juan		juanrd0088@gmail.com

Acknoledgements:
  Authors want to thank the Spanish Economy & competitiveness Ministry which funds this research 
  through "INNPACTO" innovation program IPT-2012-0839-430000.


High dimensionality (HD) problems are those which have items with high number of dimensions
There are two types of HD problems::
 a)set of items with large number of dimensions.
 b)set of items with a limited number of dimensions from a large available number of dimensions
  For example considering dimensions X, Y, Z, K, L, M and the items:
    item1=(X=2, Z=5, L=7)
    item2=(X=6, Y=5, M=7)

The HD problems involves a high cost computation because distance functions in this case takes more
operations than Low dimensionality problems.

For case "b" (valid also for "a"), a new distance for HD problems is available:  HDdistItems() ,HDequals()
This distance function compares dimensions between 2 items.
Each dimension of item1 is searched in item2, and if it is found, then the distance takes into account the difference (mahatan style)
if the dimension does not exist in item2, a maximum value is added to the total distance between item1 and item2

there is no difference with current usage::
 
 >>>cl = KMeansClustering(users,HDdistItems,HDequals);


Additionally, now the number of iterations can be limited in order to save time
Experimentally, we have concluded that 10 iterations is  enough accurate for most cases.
The new HDgetClusters() function is linear. Avoid the recalculation of centroids
whereas original function getClusters() is N*N complex, because recalculate the
centroid when move an item from one cluster to another. 
This new function can be used for low and high dimensionality problems, increasing 
performance in both cases::

 >>>solution = cl.HDgetclusters(numclusters,max_iterations)

Other new available optimization inside HDcentroid() function in is the use of mean instead median at centroid calculation.
median is more accurate but involves more computations when N is huge. 
The function HDcentroid() is invoked internally by HDgetclusters()

