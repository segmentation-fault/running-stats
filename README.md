# running-stats
Implements the running weighted mean and variance as described in: D. H. D. West. 1979. Updating mean and variance estimates: an improved method. Commun. ACM 22, 9 (September 1979), 532-535. DOI: https://doi.org/10.1145/359146.359153. It also provides a fail-safe against numerical overflow by chunking sums, preventing them from numerical overflowing.

In running_stats.py, the main is a test against the classical two pass algorithm (using numpy).

In io_stats_example.py, the main draws an animation representing the average write speed on dev/null (or nul in windows), where file sizes are drawn from a discrete uniform distribution between a and b, with b > a. It displays both the running average and     the running 95% confidence interval around the average curve.
