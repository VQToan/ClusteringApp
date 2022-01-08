import re

import numpy as np
from collections import Counter

from core.kMeans.hierarchicalKMeans import hierarchicalKMeans


def getInt(ex: str):
    if ex.isdigit():
        return int(ex)
    else:
        digitList = re.findall(r'\d', ex)
        if len(digitList) > 0:
            return int("".join([str(char) for char in digitList]))
        else:
            return None


def sortEmbedList(embed_list: list):
    for j in range(len(embed_list)):
        for i in range(len(embed_list)):
            if getInt(embed_list[i]) == None:
                embed_list.append(embed_list.pop(i))
            else:
                if i < (len(embed_list) - 2) and getInt(embed_list[i + 1]) != None:
                    if getInt(embed_list[i]) > getInt(embed_list[i + 1]):
                        tmp = embed_list[i]
                        embed_list[i] = embed_list[i + 1]
                        embed_list[i + 1] = tmp
    return embed_list

def create_embedlib(input_dataset: list, input_datasetBase: list):
    """
    dùng để tạo danh sách các thuộc tính của tập dữ liệu, dùng để số hóa tập dữ liệu
    :param input_dataset: Dữ liệu đầu vào là list các phần tử của dataset
    :param input_datasetBase: list: Dữ liệu đầu vào là list các phần tử của dataset
    :return: embedlib
    """
    embed_list = []
    for i in range(len(input_dataset[0])):
        for item in input_dataset:
            if item[i] not in embed_list:
                embed_list.append(item[i])

    for bigItem in input_datasetBase:
        for i in range(len(bigItem[0])):
            for item in bigItem:
                if item[i] not in embed_list:
                    embed_list.append(item[i])
    # print(embed_list)

    embed_lib = {}
    embed_list = sortEmbedList(embed_list)
    for val, key in enumerate(embed_list):
        embed_lib.update({key: val})
    return embed_lib


def embed(input_data: list, embed_lib):
    """
    Số hóa tập dữ liệu
    :param input_data: Dữ liệu đầu vào là list các phần tử của dataset
    :param embed_lib: library
    :return: data_embed: list
    """
    data_embed = []
    for item in input_data:
        data_embed.append([embed_lib[key] for key in item])
    return data_embed


def deemebed(data_input, embed_lib):
    """
    Giải mã dataset thành string
    :param data_input: numpy.array: ma trận đã số hóa
    :param embed_lib:
    :return: data_dembed:list
    """

    def get_key(val):
        for key, value in embed_lib.items():
            if val == value:
                return key

    data_dembed = []
    for item in data_input:
        data_dembed.append([get_key(int(val)) for val in item])
    return data_dembed


def get_index(listRQ, listHavIndex):
    """
    :param listRQ: líst: danh sách chứa các trường dùng để phân cụm
    :param listHavIndex: list: danh sách các trường của tập dữ liệu cần lấy index
    :return: result: list
    """
    result = []
    for item in listRQ:
        try:
            result.append(listHavIndex.index(item))
        except:
            continue
    return result


def dataProcessing(dataset, datasetBase, header, hearderBase, hearderClus, embed_lib):
    """
    Xử lý dữ liệu đầu vào
    :param dataset: list: tập dữ liệu cần phân cụm
    :param datasetBase: list: tập dữ liệu giống
    :param header: list : các trường dữ liệu của tập phân cụm
    :param hearderBase: list : các trường dữ liệu của tập giống
    :param hearderClus: list : các trường dữ liệu dùng để phân cụm
    :param embed_lib: libray : thư viện để số hóa tập dữ liệu
    :return: dataset, datasetBase
    """
    # số hóa
    dataset_tmp = np.array(embed(dataset, embed_lib)) / 100
    datasetBase = [np.array(embed(item, embed_lib)) / 100 for item in datasetBase]
    # Lọc các trường không cần thiết
    dataset_tmp = dataset_tmp[:, get_index(hearderClus, header)]
    listidx = get_index(hearderClus, hearderBase)
    datasetBase_tmp = []
    for item in datasetBase:
        datasetBase_tmp.append(item[:, listidx])
    return dataset_tmp, datasetBase_tmp


def summary(dataset, labels, n_cluster):
    result = []
    for i in range(n_cluster):
        data = dataset[labels == i, :]
        result.append(getMost(data))
    return np.array(result)


def getMost(datalist):
    list_tmp = []
    for k in range(datalist.shape[1]):
        list_tmp.append(Counter(datalist[:, k]).most_common()[0][0])
    return list_tmp


def getPercent(dataset, lables, n_cluster):
    listPercent = []
    total = dataset.shape[0]
    # print(total)
    for k in range(n_cluster):
        listPercent.append(((len(dataset[lables == k, :]) * 1.0) / total) * 100)
    if sum(listPercent) == 100:
        return listPercent


def runAlgorithm(dataset, datasetBase, header, hearderBase, hearderClus, kMax):
    embed_lib = create_embedlib(dataset, datasetBase)
    dataset_tmp, datasetBase_tmp = dataProcessing(dataset, datasetBase, header, hearderBase, hearderClus, embed_lib)
    cluster_action = hierarchicalKMeans(dataset_tmp, kMax, datasetBase_tmp, len(datasetBase_tmp))
    centers, labels, n_cluster = cluster_action.fit()
    listPercent = getPercent(dataset_tmp, labels, n_cluster)
    clusteredData = deemebed((summary(dataset_tmp, labels, n_cluster)) * 100, embed_lib)
    return clusteredData, listPercent, labels
