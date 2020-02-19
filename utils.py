# *_*coding:utf-8 *_*
#
import copy


class find_path():
    def __init__(self, target):
        self.target = target

    def find_the_value(self, target, value, path='', path_list=None):
        '''完全匹配，每经过一层(list、dict)都会记录path，到了最后一层且当前target就是要找的目标，才把对应的path记录下来
        :param target: 被搜索的目标
        :param value: 要搜索的关键字
        :param path: 当前所在的路径
        :param path_list: 存放所有path的列表
        判断当前target类型：···是字典，循环内容，每个键值都记录下路径path，然后以当前值v为判断target，调用自身传入添加了的path判断
                             ···是列表，循环内容，每个元素都记录下路径path，然后以当前元素为判断target，调用自身传入添加了的path判断
                             ···是str或者int，那么就判断当前target是否就是要搜索的value，如果是，那就把路径path放进list里面'''
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1 = path1 + str([k])
                self.find_the_value(v, value, path1, path_list)

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            for i in target:
                path1 = copy.deepcopy(path)
                posi = target.index(i)
                path1 = path1 + '[%s]' % posi
                self.find_the_value(i, value, path1, path_list)

        elif isinstance(target, (str, int)):
            if str(value) == str(target):  # 必须完全相同
                path_list.append(path)

    def find_in_value(self, target, value, path='', path_list=None):
        '''包含匹配，内容跟上面一样，只是最后判断时不同'''
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1 = path1 + str([k])
                self.find_in_value(v, value, path1, path_list)

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            for i in target:
                path1 = copy.deepcopy(path)
                posi = target.index(i)
                path1 = path1 + '[%s]' % posi
                self.find_in_value(i, value, path1, path_list)

        elif isinstance(target, (str, int)):
            if str(value) in str(target):  #
                path_list.append(path)

    def find_the_key(self, target, key, path='', path_list=None):
        '''查找key，每经过一层(list、dict)都会记录path，在字典时，若当前的k就是要找的key，那就把对应的path记录下来
                :param target: 被搜索的目标
                :param key: 要搜的键
                :param path: 当前所在的路径
                :param path_list: 存放所有path的列表
                判断当前target类型：···是字典，循环内容，每个键值都记录下路径path，判断当前k是否要查找的：~~~是，那就把路径path放进list里面
                                                                                                 ~~~不是，以当前值v为判断target，调用自身传入添加了的path判断
                                  ···是列表，循环内容，每个元素都记录下路径path，然后以当前元素为判断target，调用自身传入添加了的path判断
                                     '''
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1 = path1 + str([k])
                if str(key) == str(k):
                    path_list.append(path1)
                else:
                    self.find_the_key(v, key, path1, path_list)

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            for i in target:
                path1 = copy.deepcopy(path)
                posi = target.index(i)
                path1 = path1 + '[%s]' % posi
                self.find_the_key(i, key, path1, path_list)

    # ====================================================================================

    def in_value_path(self, value):
        '''包含匹配value'''
        path_list = []
        self.find_in_value(self.target, value, path_list=path_list)
        return path_list

    def the_value_path(self, value):
        '''完全匹配value'''
        path_list = []
        self.find_the_value(self.target, value, path_list=path_list)
        return path_list

    def the_key_path(self, value):
        '''只查找key'''
        path_list = []
        self.find_the_key(self.target, value, path_list=path_list)
        return path_list
