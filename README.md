Experiment on Algorithms to measure 95th and 99th percentiles

Method:

I have a big list of various random distributions from python stdlib.  I loop over the list. 
For each distribution, I perform 100 experiments.  In each experiment, I generate some # 
(10 million in the experiment which I committed the results to the repo) of random 
observations.  While generating the data, I use faststat's P2 algorithm and 3 reservoir samples
(of various sizes), to generate estimates for the values of various percentiles of the distribution. 

At the end of the 10M points, I save off the percentiles from the estimates and the "true" value from the 
full 10M points (not calculating the mathematical true value).  

At the end of those 100 experiments, I generate a mean and std dev for each of the various percentile algorithms
and print it out.  I don't calculate an error #, you can eye ball it.  

 Net results:  for ‘good’ distributions, P2 is about 10x better than reservoir, reservoir is better 2x@16k than 8k, and they all get you at least 1 sigfig of accuracy on 99.0%ile  32K reservoir sampling gets you to 2 sigfig accuracy seems like.
