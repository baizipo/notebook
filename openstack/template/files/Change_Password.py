# -*- coding: utf-8 -*-
import sys
import subprocess
import urllib2
import logging
import time


class utils(object):
    old_content = None
    @classmethod
    def send_log(cls, content):
        if not cls.old_content:
            cls.old_content = content
        if cls.old_content == content:
            return
        cls.old_content = content
        cmd = 'echo %s > com1' % content
        cls.exec_cmd(cmd)
    @classmethod
    def exec_cmd(cls, cmd):
        ret = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,)
        return ret.stdout.read(), ret.stderr.read()


class ComHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
    def emit(self, record):
        msg = self.format(record)
        utils.send_log(msg)

logger = logging.getLogger('init')
logger.setLevel(logging.DEBUG)
handler = ComHandler()
formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class network(object):
    def __init__(self):
        pass
    def get_gateway(self):
        cmd = 'route print'
        out, err = utils.exec_cmd(cmd)
        for i in out.split('\n'):
            if ('0.0.0.0' in i) and ('224.0.0.0' not in i):
                gateway = i.split()[3]
                logger.debug('Get_gateway succeed:' + gateway)
                return gateway
        if err:
            logger.debug('Get_gateway failed, msg: %s.' %err)
            time.sleep(2)

    def get_NetworkNumber(self):
        cmd = 'route print'
        out, err = utils.exec_cmd(cmd)
        for i in out.split('\n'):
            if 'Red Hat VirtIO' in i:
                NetworkNumber = i.split('.')[0]
                logger.debug('get_NetworkNumber succeed: %s'  %NetworkNumber)
                return NetworkNumber
        if err:
            logger.debug('get_NetworkNumber failed, msg: %s.' %err)
            time.sleep(2)

    def add_route(self, gateway, NetworkNumber):
        cmd = ['route', 'add', '169.254.169.254', 'mask', '255.255.255.255',
               gateway, 'metric', '10', 'if', NetworkNumber]
        out, err = utils.exec_cmd(cmd)
        if out:
            logger.debug(out)
        if err:
            logger.debug(err)

        
class Password_Handler(object):
    def __init__(self):
        pass
    def get_metadata(self):
        url = 'http://169.254.169.254/openstack/2013-04-04/meta_data.json'
        data = urllib2.urlopen(url)
        result = data.read()
        dic_result = eval(result)
        logger.debug('get_metadata succeed')
        password = dic_result['meta']['admin_pass']
        return password
    def set_password(self, password):
        cmd = ['net', 'user', 'administrator', password]
        out, err = utils.exec_cmd(cmd)
        if out:
            logger.debug('Modify password succeed')
        if err:
            logger.error('Modify password failed, password: '% password)

if __name__ == '__main__':
    # setting network
    N = network()
    gateway = None
    while not gateway:
        logger.debug('getting gateway...')
        gateway = N.get_gateway()
    NetworkNumber = None
    while not NetworkNumber:
        logger.debug('getting NetworkNumber...')
        NetworkNumber = N.get_NetworkNumber()
    N.add_route(gateway, NetworkNumber)

    # change password
    admin = Password_Handler()
    password = admin.get_metadata()
    admin.set_password(password)

    # del self
    cmd = ['del', sys.argv[0]]
    utils.exec_cmd(cmd)
