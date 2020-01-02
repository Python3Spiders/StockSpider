# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/12/2 12:25
# file_name:        myDict.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

class AllowKeyRepeatDict():
    '''
    自定义允许键重复的字典
    其本质是一个列表，列表元素为字典，核心思想是把键重复的item分散到不同字典
    封装后列表对外操作像字典
    '''
    def __init__(self):
        self.dictList = []

    def add(self,key,value):
        length = len(self.dictList)
        i = 0
        while i<length:
            if not self.dictList[i].get(key,None):
                self.dictList[i][key] = value
                return i
            i += 1
        newDict = {}
        newDict[key] = value
        self.dictList.append(newDict)
        return i

    def delete(self,key):
        '''
        :param key: 根据 key 删除所有 item
        '''
        length = len(self.dictList)
        for i in range(length):
            response = self.dictList[i].pop(key,None)
            if not response:
                break
        # 清除哪些空容器，注意从后往前删，否则会出现下标越界
        while length>0:
            if self.dictList[length-1]=={}:
                del self.dictList[length-1]
            length -= 1


    def query(self,key):
        '''
        :param key: 查询的健
        :return: 由于允许键重复，返回形式是一个列表
        '''
        result = []
        length = len(self.dictList)
        for i in range(length):
            response = self.dictList[i].get(key,None)
            if not response:
                return result
            result.append(response)
        return result

    def __str__(self):
        '''
        :return: 打印整个字典
        '''
        resStr = ''

        length = len(self.dictList)

        if length==0:
            return '该字典为空'

        for i in range(length):
            for k,v in self.dictList[i].items():
                aItem = 'key:{:<8}value:{:<8}\n'.format(k,v)
                resStr += aItem

        return  resStr



