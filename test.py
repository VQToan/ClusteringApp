import random

import numpy as np
from matplotlib import pyplot as plt
from algorithm_lib.hierarchicalKMeans import hierarchicalKMeans


def kmeans_visualize(X, centers, labels, n_cluster, title):
    plt.xlabel('x')  # label trục x
    plt.ylabel('y')  # label trục y
    plt.title(title)  # title của đồ thị
    plt_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # danh sách các màu hỗ trợ

    for i in range(n_cluster):
        data = X[labels == i]  # lấy dữ liệu của cụm i
        plt.plot(data[:, 0], data[:, 1], random.choice(plt_colors) + '^', markersize=4,
                 label='cluster_' + str(i))  # Vẽ cụm i lên đồ thị
        plt.plot(centers[i][0], centers[i][1], random.choice(plt_colors) + 'o', markersize=10,
                 label='center_' + str(i))  # Vẽ tâm cụm i lên đồ thị
    plt.legend()  # Hiện bảng chú thích
    plt.show()


# Tạo bộ dữ liệu
means = [[2, 2], [9, 2], [4, 9]]
cov = [[2, 0], [0, 2]]
n_samples = 20
n_cluster = 3
X0 = np.random.multivariate_normal(means[0], cov, n_samples)
X1 = np.random.multivariate_normal(means[1], cov, n_samples)
X2 = np.random.multivariate_normal(means[2], cov, n_samples)

dataset_base = [X0, X1, X2]
cov = [[6, 0], [0, 6]]
dataset = np.random.multivariate_normal((6, 6), cov, 2000)

plt.xlabel('x')
plt.ylabel('y')
plt.plot(dataset[:, 0], dataset[:, 1], 'bo', markersize=5)
plt.plot()
plt.show()

cluster_action = hierarchicalKMeans(dataset, 7, dataset_base, 3)
centers, labels, n_cluster = cluster_action.fit()
# print(centers)
kmeans_visualize(dataset, centers, labels, n_cluster, "Done")
