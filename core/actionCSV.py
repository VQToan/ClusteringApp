import csv


def cluseringByCell(dataset: list, idCell: int):
    list_key = []
    for item in dataset:
        if item[idCell] not in list_key:
            list_key.append(item[idCell])
    data_clustered = []
    for key in list_key:
        cluster = []
        for item in dataset:
            if item[idCell] == key:
                cluster.append(item)
        data_clustered.append(cluster)
    return data_clustered, list_key


def readDataset(filePath):
    dataset_tmp = []
    with open(filePath, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        hearder = csv_reader.fieldnames
        for row in csv_reader:
            dataset_tmp.append(list(row.values()))
    return dataset_tmp, hearder


def saveResult(filePath, dataset, labels, n_cluster, header: list):
    with open(filePath, 'w', newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if "Nhóm" not in header:
            header.insert(0, "Nhóm")
        writer.writerow(header)
        for k in range(n_cluster):
            dataset_tmp = dataset[labels == k, :]
            print(type(dataset_tmp))
            for item in dataset_tmp:
                tmp=list(item)
                tmp.insert(0, k+1)
                # print(tmp)
                writer.writerow(tmp)
# result_deembed = deemebed((summary(dataset, labels, n_cluster)) * 100, embed_lib)
# for item in result_deembed:
#     print(item)
# with open('result.csv', 'w', newline='', encoding="utf-8-sig") as f:
#     writer = csv.writer(f)
#     writer.writerow(hearder)
#     for item in result_deembed:
# #         data = deemebed((dataset[labels == k, :]) * 100, embed_lib)
# #         # print((dataset[labels == k, :]) * 100)
# #         # print(data)
# #         # print((dataset[labels==k,:])*100)
#         writer.writerow(item)
# #         writer.writerow([0 for i in range(dataset.shape[1])])
