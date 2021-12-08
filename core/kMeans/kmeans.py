import numpy as np
from scipy.spatial.distance import cdist


class printException(Exception):
    def __init__(self, value):
        print("Error: " + value)


class K_means:
    def kmeans_init_centers(self, X, n_cluster):
        # random k index beetween 0 and shape(X) without duplicate index.
        # Then return X[index] as cluster
        return X[np.random.choice(X.shape[0], n_cluster, replace=False)]

    def kmeans_predict_labels(self, X, centers):
        D = cdist(X, centers)
        # return index of the closest center
        return np.argmin(D, axis=1)

    def kmeans_update_centers(self, X, labels, n_cluster):
        centers = np.zeros((n_cluster, X.shape[1]))
        for k in range(n_cluster):
            # collect all points assigned to the k-th cluster
            Xk = X[labels == k, :]
            # take average
            centers[k, :] = np.mean(Xk, axis=0)
            # print(centers[k, :])
        return centers

    def kmeans_has_converged(self, centers, new_centers):
        # return True if two sets of centers are the same
        return (set([tuple(a) for a in centers]) ==
                set([tuple(a) for a in new_centers]))

    def kmeans(self, X, centers, n_cluster):
        while True:
            labels = self.kmeans_predict_labels(X, centers)
            new_centers = self.kmeans_update_centers(X, labels, n_cluster)
            if self.kmeans_has_converged(centers, new_centers):
                break
            centers = new_centers
        return centers, labels

    def fit(self, X, n_cluster):
        centers = self.kmeans_init_centers(X, n_cluster)
        centers, labels = self.kmeans(X, centers, n_cluster)
        return centers, labels


class BIC:
    """

    """

    def __init__(self):
        pass

    def n_param(self, n_clusters, n_dims):
        return n_clusters * (n_dims + 1)

    def log_likelihood(self, n_points, n_dims, clusters, centers):
        ll = 0
        for cluster in clusters:
            fRn = len(cluster)
            # print(fRn)
            t1 = fRn * np.log(fRn)
            t2 = fRn * np.log(n_points)
            variance = max(self.cluster_variance(n_dims, clusters, n_points, centers),
                           np.nextafter(0, 1))
            t3 = ((fRn * n_dims) / 2.0) * np.log((2.0 * np.pi) * variance)
            t4 = n_dims * (fRn - 1.0) / 2.0
            ll += t1 - t2 - t3 - t4
        return ll

    def cluster_variance(self, n_dims, clusters, n_points, centers):
        s = 0
        denom = float(n_points - len(centers)) * n_dims
        if denom <= 0: return 0
        for cluster, centroid in zip(clusters, centers):
            distances = cdist(cluster, [centroid])
            s += (distances * distances).sum()
        return s / denom

    def calculate(self, clusters, centers, n_clusters):
        # print([len(cluster) for cluster in clusters])
        self.check_input_format(clusters, centers, n_clusters)
        n_dims = clusters[0].shape[1]
        n_points = sum(len(cluster) for cluster in clusters)

        BIC = -(self.n_param(n_clusters, n_dims) * np.log10(n_points)) + 2 * self.log_likelihood(n_points, n_dims,
                                                                                               clusters, centers)
        # BIC = self.log_likelihood(n_points, n_dims, clusters, centers) - self.n_param(n_clusters,n_dims) / 2.0 * np.log(n_points)
        # print(BIC)
        return BIC

    def check_input_format(self, clusters, centers, n_clusters):
        if len(clusters) != n_clusters:
            raise printException("Cluster input is incorrect format")
        # print(centers)
        # print(centers.shape[0])
        # print(n_clusters)
        if centers.shape[0] != n_clusters:
            raise printException("num_cluster or num_centers is incorrect")
        n_dims = clusters[0].shape[1]
        for cluster in clusters:
            if cluster.shape[1] != n_dims:
                raise printException("num_dims is incorrect between clusters")
