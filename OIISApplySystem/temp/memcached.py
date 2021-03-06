# coding=utf-8
# author: Lan_zhijiang
# description: 操作memcached数据库
# date: 2020/10/2

import memcache


class MemcachedManipulator:

    def __init__(self, addr, port):

        self.mc = memcache.Client(
            [addr+":"+str(port)]
        )

    def _set(self, key, value):

        """
        设置键值（若键存在，则replace，若键不存在，则add）
        :param key 键
        :param value 值
        :return bool
        """
        if type(key) == int or type(key) == str or type(key) == float:
            print("MemcachedManipulator: Set: key " + str(key) + " value: " + str(value))
            self.mc.set(key, value)  # Add some exception
            return True

        print("MemcachedManipulator: key can't be a list or dict")
        return False

    def _add(self, key, value):

        """
        添加（未存在的键）的值
        :param key 键
        :param value 值
        :return bool
        """
        if type(key) == int or type(key) == str or type(key) == float:
            print("MemcachedManipulator: Add: key " + str(key) + " value: " + str(value))
            try:
                self.mc.add(key, value)
            except self.mc.MemcachedKeyError:
                print("MemcachedManipulator: Add failed: there is already a key called " + str(key))
                return False
            else:
                return True

        print("MemcachedManipulator: key can't be a list or dict")
        return False

    def _replace(self, key, value):

        """
        替换（已存在键）的值
        :param key 键
        :param value 值
        :return bool
        """
        if type(key) == int or type(key) == str or type(key) == float:
            print("MemcachedManipulator: Replace: key " + str(key) + " value: " + str(value))
            self.mc = self.mc.replace(key, value)
            return True

        print("MemcachedManipulator: key can't be a list or dict")
        return False

    def _set_multi(self, param):

        """
        设置多个键值
        :param param dict形式的数据
        :return bool
        """
        if type(param) == dict:
            print("MemcachedManipulator: Multi set: key to value: " + str(param))
            self.mc.set_multi(param)
            return True

        print("MemcachedManipulator: In set multi, the param must be a dict!")
        return False

    def _delete(self, key):

        """
        删除一个键值
        :param key: 要删除的键（同时删除了值）
        :return bool
        """
        if type(key) == int or type(key) == str or type(key) == float:
            print("MemcachedManipulator: Delete: key: " + str(key))
            self.mc.delete(key)
            return True

        print("MemcachedManipulator: key can't be a list or dict")
        return False

    def _delete_multi(self, param):

        """
        删除多个键值
        :param param: 要删除的键的list
        :return bool
        """
        if type(param) == list or type(param) == tuple:
            print("MemcachedManipulator: Delete: keys: " + str(param))
            self.mc.delete_multi(param)
            return True

        print("MemcachedManipulator: In delete multi, param must be a list")
        return False

    def _get(self, key):

        """
        获取键的值
        :param key 键
        :return any
        """
        if type(key) == int or type(key) == str or type(key) == float:
            print("MemcachedManipulator: Get: key: " + str(key))
            try:
                return self.mc.get(key)
            except self.mc.MemcachedKeyError:
                print("MemcachedManipulator: key: " + str(key) + "not found!")
                return None

        print("MemcachedManipulator: key can't be a list or dict")
        return None

    def _get_multi(self, param):

        """
        获取多个键的值
        :param param: 要获取的键的list
        :return any
        """
        if type(param) == list or type(param) == tuple:
            print("MemcachedManipulator: Get multi: keys: " + str(param))
            return self.mc.get_multi(param)

        print("MemcachedManipulator: key can't be a list or dict")
        return None

    def _increase(self, key):

        """
        key的值自加
        :param key 键
        :return bool
        """
        if type(key) != int or type(key) != str or type(key) != float:
            print("MemcachedManipulator: key can't be a list or dict")
            return False

        print("MemcachedManipulator: Self increase: key: " + str(key))
        self.mc.incr(key)
        return True

    def _decrease(self, key):

        """
        key的值自减
        :param key 键
        :return bool
        """
        if type(key) != int or type(key) != str or type(key) != float:
            print("MemcachedManipulator: key can't be a list or dict")
            return False

        print("MemcachedManipulator: Self decrease: key: " + str(key))
        self.mc.decr(key)
        return True

    def return_mc(self):

        """
        返回连接着的memcached数据库操作class
        :return class
        """
        return self.mc

    def disconnect(self):

        """
        断开当前连接的memcached数据库
        :return
        """
        self.mc.disconnect_all()

    def connect_to_new(self, database_name):

        """
        连接到新的memcached数据库
        :return
        """
        self.disconnect()
        self.database_name = database_name
        try:
            self.memcached_server_address = self.memcached_settings["address"][database_name]
        except KeyError:
            print("MemcachedManipulator: Can't find memcached server named: "
                             + database_name + "'s address in the settings, please check it.")

        self.mc = memcache.Client(
            [self.memcached_server_address]
        )

