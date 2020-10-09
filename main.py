#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkdcdn.request.v20180115.DescribeDcdnDomainLogRequest import DescribeDcdnDomainLogRequest
import json
import configparser
import wget
import os


def get_section_by_key(section, key_list):
    """
    :param section:
    :param key_list:
    :return:
    """
    item = dict()
    for key in key_list:
        item[key] = section[key]
    return item


def run():
    # init
    config = configparser.ConfigParser()
    filepath = 'config.ini'
    if not os.path.exists(filepath):
        exit('config file is not exist. ')
    config.read(filepath)

    for domain in config.sections():
        domain_config = config[domain]
        connect_config = get_section_by_key(domain_config, ['ak', 'secret', 'region_id'])

        client = AcsClient(**connect_config)

        request = DescribeDcdnDomainLogRequest()
        request.set_accept_format('json')

        request.set_DomainName(domain)

        response = client.do_action_with_exception(request)

        response_json = json.loads(str(response, encoding='utf-8'))

        protocol = "http://"
        log_urls = [protocol + log['LogPath'] for log in
                    response_json['DomainLogDetails']['DomainLogDetail'][0]['LogInfos']['LogInfoDetail']]
        output_directory = os.path.join(os.getcwd(), "logs", domain)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for url in log_urls:
            wget.download(url, out=output_directory)


if __name__ == '__main__':
    run()
