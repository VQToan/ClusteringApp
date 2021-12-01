import random


from algorithm_lib.seeded_kmeans import Seeded_KMeans
from algorithm_lib.kmeans import *


class hierarchicalKMeans:
    def __init__(self, dataset, k_max, base_dataset, k_min):
        """
        :param dataset: numpy.array : tập cần phân cụm: không bị trùng lặp dữ liệu
        :param k_max: int : số cụm tối đa : 1 trong các điều kiện dừng thuật toán
        :param base_dataset: numpy.array: tập giống -> tập mẫu đã phân cụm
        :param k_min: int : Số cụm tối thiểu: số cụm theo tập giống
        """
        self.s_KMeans = Seeded_KMeans()
        self.kMeans = K_means()
        self.BIC = BIC()
        self.dataset = dataset
        self.position_data = list(dataset)
        self.k_max = k_max
        self.base_dataset = base_dataset
        self.n_cluster = k_min
        self.total_BIC = 0

    def check_converged(self):
        # print(self.labels)
        BIC_now = self.BIC.calculate([self.dataset[self.labels == i, :] for i in range(self.n_cluster)],
                                     self.centers, self.n_cluster)
        if BIC_now == self.total_BIC:
            return True
        if self.n_cluster >= self.k_max:
            return True
        self.total_BIC = BIC_now
        return False

    def fit(self):
        # Bước 1: Chạy thuật toán Seed-KMeans
        self.centers, self.labels = self.s_KMeans.fit(self.base_dataset, self.n_cluster, self.dataset)
        self.total_BIC = self.BIC.calculate([self.dataset[self.labels == i, :] for i in range(self.n_cluster)],
                                            self.centers, self.n_cluster)
        # print(self.labels)
        # Bước 2 + 3: vòng lặp
        while True:
            centers_tmp = []
            lables_tmp =list(self.labels)
            n_clusters_tmp = 0
            for k in range(self.n_cluster):
                dataset_sep = self.dataset[self.labels == k, :]
                # print(self.centers[k,:])
                BIC_before = self.BIC.calculate([dataset_sep], np.array([self.centers[k, :]]), 1)
                centers, labels = self.kMeans.fit(dataset_sep, 2)
                BIC_after = self.BIC.calculate([dataset_sep[labels == i, :] for i in range(2)], centers, 2)
                # print(n_clusters_tmp)
                if BIC_after > BIC_before:
                    centers_tmp.extend(list(centers))
                    labels = list(labels)
                    for i in range(0, len(self.labels)):
                        if self.labels[i] == k:
                            lables_tmp[i] = int(labels.pop(0) + n_clusters_tmp)
                    n_clusters_tmp += 2
                else:
                    centers_tmp.append(self.centers[k, :])
                    for i in range(0, len(self.labels)):
                        if self.labels[i] == k:
                            lables_tmp[i] = int(n_clusters_tmp)
                    n_clusters_tmp += 1
            self.centers = np.array(centers_tmp)
            self.labels = np.array(lables_tmp)
            self.n_cluster = n_clusters_tmp
            # kmeans_visualize(self.dataset, self.centers, self.labels, self.n_cluster, "Done")
            if self.check_converged():
                break
        return self.centers, self.labels, self.n_cluster
