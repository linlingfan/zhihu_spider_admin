# __author_="gLinlf"
# coding=utf-8


class CommUtils(object):
    # 参数部位None 验证
    @staticmethod
    def check_params(*args):
        result = True
        if None in args:
            result = False
        return result

    # 将字典类型转成list（用于字典key 或value排序）
    @staticmethod
    def dict2list(dic: dict):
        ''' 将字典转化为列表 '''
        keys = dic.keys()
        vals = dic.values()
        lst = [(key, val) for key, val in zip(keys, vals)]
        return lst

        # dic = {'a': 4, 'b': 2, 'c': 1, 'd': 5}
        # 按照第0个元素降序排列
        # dic = sorted(dict2list(dic), key=lambda x: x[0], reverse=False)
        # 按照第1个元素降序排列
        # dic = sorted(dict2list(dic), key=lambda x: x[1], reverse=True)
        # print(dic)
    # 参数是否为空 不为None和 ''长度大于0
    @staticmethod
    def is_not_empty(parm):
        if parm is not None and len(str(parm).strip()) > 0:
            return True
        else:
            return False


if __name__ == '__main__':
    # print(CommUtils.check_params(1))
    print(not CommUtils.is_not_empty(' '))
