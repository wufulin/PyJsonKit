# encoding=utf-8

__author__ = 'wufulin'
__version__ = '1.0.0'

import Tool
import re


class JsonParser(object):
    item_separator = ','
    key_separator = ':'

    # encode python object to json object
    def _encode_string(self, obj):
        """
        返回JSON string,表示Python string
        """
        ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
        ESCAPE_DCT = {
            '\\': '\\\\',
            '"': '\\"',
            '\b': '\\b',
            '\f': '\\f',
            '\n': '\\n',
            '\r': '\\r',
            '\t': '\\t',
        }

        def replace(match):
            return ESCAPE_DCT[match.group(0)]

        return '"' + ESCAPE.sub(replace, obj) + '"'

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
                buf += self._encode_string(value)
            elif value is None:
                buf += self._encode_null()
            elif isinstance(value, bool):
                buf += self._encode_bool(value)
            elif isinstance(value, (int, long, float)):
                buf += self._encode_number(value)
            elif isinstance(value, (list, tuple)):
                buf += self._encode_array(value, level)
            elif isinstance(value, dict):
                buf += self._encode_object(value, 0)
        buf += ']'

        return buf

    def _encode_object(self, dct, level):
        if not dct:
            return '{}'

        buf = '{'
        first = True
        level += 1
        items = dct.iteritems()

        for key, value in items:
            if isinstance(key, basestring):
                pass
            elif isinstance(key, float):
                key = self._encode_number(key)
            elif key is True:
                key = 'true'
            elif key is False:
                key = 'false'
            elif key is None:
                key = 'null'
            elif isinstance(key, (int, long)):
                key = str(key)
            else:
                raise TypeError("key " + repr(key) + " is not a string")
            if first:
                first = False
            else:
                buf += self.item_separator
            buf += self._encode_string(key)
            buf += self.key_separator

            if isinstance(value, basestring):
                buf += self._encode_string(value)
            elif value is None:
                buf += 'null'
            elif value is True:
                buf += 'true'
            elif value is False:
                buf += 'false'
            elif isinstance(value, (int, long)):
                buf += str(value)
            elif isinstance(value, float):
                buf += self._encode_number(value)
            else:
                if isinstance(value, (list, tuple)):
                    buf += self._encode_array(value, 0)
                elif isinstance(value, dict):
                    buf += self._encode_object(value, level)
        buf += '}'
        return buf

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

    #def _object_dict(self, obj):
    #    d = {}
    #    d.update(obj.__dict__)
    #    return d

    # decode json object to python object.
    def _decode(self, string, index):

        nextchar = string[index]

        if nextchar == '"':
            return self._decode_string(string, index + 1)
        elif nextchar == '{':
            return self._decode_dict(string, index + 1)
        elif nextchar == '[':
            return self._decode_list(string, index + 1)
        elif nextchar == 'n' and string[index:index + 4] == 'null':
            return self._decode_none(index)
        elif nextchar == 't' and string[index:index + 4] == 'true':
            return self._decode_true(index)
        elif nextchar == 'f' and string[index:index + 5] == 'false':
            return self._decode_false(index)

        if nextchar == '-' or \
                (nextchar == '0' and string[index + 1] not in Tool.DIGIT) or ('1' <= nextchar <= '9'):
            return self._decode_float_int(string, index)
        elif nextchar == 'N' and string[index:index + 3] == 'NaN':
            return 'NaN', index + 3
        elif nextchar == 'I' and string[index:index + 8] == 'Infinity':
            return 'Inf', index + 8
        elif nextchar == '-' and string[index:index + 9] == '-Infinity':
            return '-Inf', index + 9
        else:
            raise StopIteration

    def _decode_string(self, string, index):
        values = []
        nextchar = string[index:index + 1]

        while True:
            if nextchar == '"':
                index += 1
                break
            elif nextchar == '\\':
                index += 1
                nextchar = string[index:index + 1]
                if nextchar == '\"':
                    values.append('\"')
                elif nextchar == '\'':
                    values.append('\'')
                elif nextchar == '\\':
                    values.append('\\')
                elif nextchar == '/':
                    values.append('/')
                elif nextchar == 'b':
                    values.append('\b')
                elif nextchar == 'f':
                    values.append('\f')
                elif nextchar == 'n':
                    values.append('\n')
                elif nextchar == 'r':
                    values.append('\r')
                elif nextchar == 't':
                    values.append('\t')
                elif nextchar == 'u':
                    esc = string[index + 1:index + 5]
                    index += 4
                    uni = int(esc, 16)
                    values.append(unichr(uni))
            else:
                values.append(nextchar)
            index += 1
            nextchar = string[index:index + 1]

        return u''.join(values), index

    def _decode_list(self, string, index):
        values = []
        nextchar = string[index:index + 1]
        if nextchar in Tool.WhiteSpace:
            index = Tool.escape_whitespace(string, index + 1)
            nextchar = string[index:index + 1]

        if nextchar == ']':
            return values, index + 1

        while True:
            try:
                value, index = self._decode(string, index)
            except StopIteration:
                raise ValueError(Tool.errmsg("Expecting object", string, index))

            values.append(value)
            nextchar = string[index:index + 1]
            if nextchar in Tool.WhiteSpace:
                index = Tool.escape_whitespace(string, index + 1)
                nextchar = string[index:index + 1]
            index += 1
            if nextchar == ']':
                break
            elif nextchar != ',':
                raise ValueError(Tool.errmsg("Expecting , delimiter", string, index))

            try:
                if string[index] in Tool.WhiteSpace:
                    index += 1
                    if string[index] in Tool.WhiteSpace:
                        index = Tool.escape_whitespace(string, index + 1)
            except IndexError:
                pass

        return values, index

    def _decode_dict(self, string, index):
        values = []
        nextchar = string[index:index + 1]

        if nextchar != '"':
            if nextchar in Tool.WhiteSpace:
                index = Tool.escape_whitespace(string, index)
                nextchar = string[index:index + 1]

            if nextchar == '}':
                values = {}
                return values, index + 1
            elif nextchar != '"':
                raise ValueError(Tool.errmsg("Expecting property name", string, index))

        index += 1

        while True:
            key, index = self._decode_string(string, index)

            if string[index: index + 1] != ':':
                index = Tool.escape_whitespace(string, index)
                if string[index:index + 1] != ':':
                    raise ValueError(Tool.errmsg("Expecting : delimiter", string, index))

            index += 1

            try:
                if string[index] in Tool.WhiteSpace:
                    index += 1
                    if string[index] in Tool.WhiteSpace:
                        index = Tool.escape_whitespace(string, index + 1)
            except IndexError:
                pass

            try:
                value, index = self._decode(string, index)
            except StopIteration:
                raise ValueError(Tool.errmsg("Expecting object", string, index))

            values.append((key, value))

            try:
                nextchar = string[index]
                if nextchar in Tool.WhiteSpace:
                    index = Tool.escape_whitespace(string, index)
                    nextchar = string[index]
            except IndexError:
                nextchar = ''
            index += 1

            if nextchar == '}':
                break
            elif nextchar != ',':
                raise ValueError(Tool.errmsg("Expecting , delimiter", string, index))

            try:
                nextchar = string[index]
                if nextchar in Tool.WhiteSpace:
                    index += 1
                    nextchar = string[index]
                    if nextchar in Tool.WhiteSpace:
                        index = Tool.escape_whitespace(string, index + 1)
                        nextchar = string[index]
            except IndexError:
                nextchar = ''

            index += 1
            if nextchar != '"':
                raise ValueError(Tool.errmsg("Expecting property name", string, index))

        values = dict(values)

        return values, index

    def _decode_float_int(self, string, index):
        integer = ''
        frac = ''
        exp = ''
        isInt = True
        isFrac = False
        isExp = False

        while True:
            if len(string) == index:
                break
            nextchar = string[index]

            if nextchar in Tool.WhiteSpace:
                index = Tool.escape_whitespace(string, index)
            elif nextchar == '-' or nextchar == '+' or ('0' <= nextchar <= '9'):
                if isInt:
                    integer += nextchar
                    index += 1
                elif isFrac and not isExp:
                    frac += nextchar
                    index += 1
                elif isExp:
                    exp += nextchar
                    index += 1
            elif nextchar == '.':
                isInt = False
                isFrac = True
                frac += nextchar
                index += 1
            elif nextchar == 'e' or nextchar == 'E':
                isExp = True
                exp += nextchar
                index += 1
            else:
                break

        if isFrac:
            res = float(integer + frac + exp)
        else:
            res = int(integer)

        return res, index

    def _decode_true(self, index):
        return True, index + 4

    def _decode_false(self, index):
        return False, index + 5

    def _decode_none(self, index):
        return None, index + 4

    def load(self, source):
        """
        读取json格式数据，source为json字符串。若遇到json格式错误，抛出异常。
        """
        start = Tool.escape_whitespace(source, 0)
        obj, end = self._decode(source, start)
        end = Tool.escape_whitespace(source, end)
        if end != len(source):
            raise ValueError(Tool.errmsg("Extra data", source, end, len(source)))
        return obj

    def dump(self, obj):
        """
        根据python数据, 返回其json格式表示形式。
        """
        if obj is None:
            return self._encode_null()
        elif isinstance(obj, bool):
            return self._encode_bool(obj)
        elif isinstance(obj, (int, long, float)):
            return self._encode_number(obj)
        elif isinstance(obj, (list, tuple)):
            return self._encode_array(obj, 0)
        elif isinstance(obj, dict):
            return self._encode_object(obj, 0)

    def loadJson(self, filePath):
        """
        从文件中读入json格式数据，filePath为文件路径，文件操作失败或者json格式错误，都抛出异常。
        """
        try:
            file = open(filePath, 'r')
            json = file.read()
            return self.load(json)
        except Exception, e:
            print(" Read %s file Error, reason --> %s" % (filePath, e.message))
        finally:
            file.close()

    def dumpJson(self, filePath, obj):
        """
        将obj中的内容以json格式存入文件，文件若存在则覆盖，文件操作失败抛出异常。
        """
        json = self.dump(obj)
        try:
            file = open(filePath, 'w')
            file.write(json)
        except Exception, e:
            print(" Write Json to %s file Error, reason --> %s" % (filePath, e.message))
        finally:
            file.close()

    def loadDict(self, dct):
        """
        读取字典中的数据，存入类中，若遇到不是字符串的key则忽略。
        """
        return self.load(dct)

    def dumpDict(self, obj):
        """
        返回一个字典，包含类中数据
        """
        if not isinstance(obj, dict):
            raise TypeError("dct must be dict type")
        else:
            return self.dump(obj)