# encoding=utf-8

__author__ = 'wufulin'
__version__ = '1.0.0'

import Tool

class JsonParser(object):

    item_separator = ','
    key_separator = ':'

    def _encode_string(self, obj):
        """
        返回JSON string,表示Python string
        """
        pass

    def _encode_array(self, lst, level):
        if not lst:
            return '[]'

        buf = '['
        first = True
        level += 1
        for value in lst:
            if first:
                first = False
            else:
                buf += self.item_separator

            if isinstance(value, basestring):
                pass
            elif value is None:
                buf += self._encode_null()
            elif isinstance(value, bool):
                buf += self._encode_bool(value)
            elif isinstance(value, (int, long, float)):
                buf += self._encode_number(value)
            elif isinstance(value, (list, tuple)):
                buf += self._encode_array(value, level)
            elif isinstance(value, dict):
                pass
        buf += ']'

        return buf

    def _encode_object(self, obj):
        pass

    def _encode_number(self, obj):
        if isinstance(obj, float):
            if obj == Tool.NaN or obj == Tool.Inf or obj == -Tool.Inf:
                raise ValueError("超出浮点数值范围: " + repr(obj))
            return repr(obj)
        elif isinstance(obj, (int, long)):
            return str(obj)

    def _encode_bool(self, obj):
        return str(obj).lower()

    def _encode_null(self):
        return str('null')

    def _object_dict(self, obj):
        d = {}
        d.update(obj.__dict__)
        return d

    def load(self, source):
        """
        读取json格式数据，source为json字符串，无返回值。若遇到json格式错误，抛出异常。
        json中数字如果超过python里的浮点数上限，也抛出异常。
        """
        pass

    def dump(self, obj):
        """
        根据类中数据返回json字符串。
        """
        if obj is None:
            return self._encode_null()
        elif isinstance(obj, bool):
            return self._encode_bool(obj)
        elif isinstance(obj, (int, long, float)):
            return self._encode_number(obj)
        elif isinstance(obj, (list, tuple)):
            return self._encode_array(obj, 0)

    def loadJson(self, filePath):
        """
        从文件中读入json格式数据，filePath为文件路径，文件操作失败或者json格式错误，都抛出异常。
        """
        pass

    def dumpJson(self, filePath):
        """
        将类中的内容以json格式存入文件，文件若存在则覆盖，文件操作失败抛出异常。
        """
        pass

    def loadDict(self, dict):
        """
        读取字典中的数据，存入类中，若遇到不是字符串的key则忽略。
        """
        pass

    def dumpDict(self):
        """
        返回一个字典，包含类中数据
        """
        pass

    def update(self, dict):
        pass

if __name__ == '__main__':
    parser = JsonParser()
