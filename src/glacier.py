#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: glacier

:Synopsis:

:Author:
    servilla
  
:Created:
    1/16/17
"""

import logging
logger = logging.getLogger('glacier')

import boto3
from botocore import utils


class Glacier(object):

    def __init__(self,vault_name=None):
        self.vault_name = vault_name
        self.client = boto3.client('glacier')


    def do_multipart_upload(self, archive=None, archive_description='',
                            part_size='4194304'):

        response = self.client.initiate_multipart_upload(
            vaultName=self.vault_name,
            archiveDescription=archive_description,
            partSize=part_size)
        location = response['location']
        upload_id = response['uploadId']

        block_size = (1024 ** 2) * 4  # 4MB
        range_start = 0

        try:
            with open(archive, 'rb') as f:
                block = f.read(block_size)
                while block:
                    bytes = len(block)
                    range = 'bytes ' + str(range_start) + '-' + \
                            str(range_start + bytes - 1) + '/*'

                    self.client.upload_multipart_part(
                        vaultName=self.vault_name,
                        uploadId=upload_id,
                        range=range,
                        body=block)

                    range_start = range_start + bytes
                    block = f.read(block_size)

                f.close()
                archive_size = str(range_start)
            upload_response = self.client.complete_multipart_upload(
                vaultName=self.vault_name,
                uploadId=upload_id,
                archiveSize=archive_size,
                checksum=utils.calculate_tree_hash(open(archive, 'rb')))
            return upload_response
        except:
            self.client.abort_multipart_upload(vaultName=self.vault_name,
                                               uploadId=upload_id)
            err_msg = 'Failed to upload archive: {archive}'.format(
                archive=archive)
            raise MultipartUploadError(err_msg)


    def do_upload(self, archive=None, archive_description=''):

        try:
            f = open(archive, 'rb')
            block = f.read()
            upload_response = self.client.upload_archive(
                vaultName=self.vault_name,
                archiveDescription=archive_description, body=block)
            f.close()
            return upload_response
        except:
            err_msg = 'Failed to upload archive: {archive}'.format(
                archive=archive)
            raise UploadError(err_msg)


class MultipartUploadError(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)



class UploadError(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)




def main():
    return 0


if __name__ == "__main__":
    main()