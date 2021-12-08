import numpy as np  # thư viện tính toán toán học
from .kmeans import K_means


class Seeded_KMeans(K_means):
    def fit_(self, arrBase, n_cluster, arrCluster):
        """
        :param arrBase: numpy.array: cụm đã được phân cụm, là tập giống có dạng mảng [cụm 1, cụm 2,...]
        :param n_cluster: int : là số cụm đã phân ở arrBase
        :param arrCluster: numpy.array: chứa các điểm dữ liệu cần phân cụm
        :return: centers:numpy.array: tập tâm của từng cụm , arrClusted: numpy.array: các tập cụm ứng với tâm đã phân cụm
        """
        # Khởi tạo các tâm từ tập giống
        init_centers = self.S_kmeans_init_centers(arrBase, n_cluster)
        # chạy thuật toán
        # print(arrCluster)
        centers, labels = self.kmeans(arrCluster,init_centers, n_cluster)
        return centers, labels

    # khởi tạo tâm cụm từ tập ban đầu
    def S_kmeans_init_centers(self, X, n_cluster):
        # X là mảng gôm các cụm đã phân cụm
        # ví dụ: X= [X0,X1,X2]
        if not self.check_base_cluster(X, n_cluster):
            raise "Cluster is False"
        centers = np.zeros((n_cluster, X[0].shape[1]))
        for k in range(n_cluster):
            centers[k, :] = np.mean(X[k], axis=0)
        return centers

    def check_base_cluster(self, clusters, n_cluster: int):
        if len(clusters) != n_cluster:
            return False
        n_dims = clusters[0].shape[1]
        for cluster in clusters:
            if cluster.shape[1] != n_dims:
                return False
        return True
