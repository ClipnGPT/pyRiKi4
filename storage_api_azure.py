#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime
import codecs

import subprocess

from azure.storage.blob import BlockBlobService, PublicAccess



# azure blob
import storage_api_azure_key as azure_key



class StorageAPI:

    def __init__(self, ):
        self.timeOut   = 10
        self.blob_account = None
        self.blob_key     = None
        self.blob_service = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, account, key, ):
        # azure blob
        if (api == 'blob'):
            try:
                # Service connect
                block_blob_service = BlockBlobService(
                    account_name = account, 
                    account_key  = key,
                    )

                self.blob_account = account
                self.blob_key     = key
                self.blob_service = block_blob_service

                #block_blob_service = None
                return True

            except Exception as e:
                pass

        self.blob_service = None
        return False



    def blob_put(self, container='default', inpPath='', inpFile='', blobFile='', ):
        if (blobFile == ''):
            blobFile = inpFile
        if (self.blob_service is None):
            print('AZURE: Not Authenticate Error !')
            return False

        try:
            # Service connect
            #block_blob_service = BlockBlobService(
            #    account_name = self.blob_account, 
            #    account_key  = self.blob_key,
            #    )
            block_blob_service = self.blob_service

            # Create a container
            block_blob_service.create_container(container)

            # Set the permission, public.
            # block_blob_service.set_container_acl(container, public_access=PublicAccess.Container)

            # Upload file
            full_path_file = inpPath + inpFile
            block_blob_service.create_blob_from_path(container, blobFile, full_path_file)

            #block_blob_service = None
            return True

        except Exception as e:
            pass

        return False

    def blob_dir(self, container='default', ):
        if (self.blob_service is None):
            print('AZURE: Not Authenticate Error !')
            return False

        try:
            # Service connect
            #block_blob_service = BlockBlobService(
            #    account_name = self.blob_account, 
            #    account_key  = self.blob_key,
            #    )
            block_blob_service = self.blob_service

            # List blobs
            blobFiles = []
            list_blobs = block_blob_service.list_blobs(container)
            for blob in list_blobs:
                blobFiles.append(blob.name)
                #print(blob.name)

            #block_blob_service = None
            return blobFiles

        except Exception as e:
            pass

        return False

    def blob_get(self, container='default', blobFile='', outPath='', outFile='', ):
        if (outFile == ''):
            outFile = blobFile
        if (self.blob_service is None):
            print('AZURE: Not Authenticate Error !')
            return False

        try:
            # Service connect
            #block_blob_service = BlockBlobService(
            #    account_name = self.blob_account, 
            #    account_key  = self.blob_key,
            #    )
            block_blob_service = self.blob_service

            # 存在検査
            if (block_blob_service.exists(container, blobFile) == True):

                # Download file
                full_path_file = outPath + outFile
                block_blob_service.get_blob_to_path(container, blobFile, full_path_file)

                #block_blob_service = None
                return True

        except Exception as e:
            pass

        return False



if __name__ == '__main__':

        #azureAPI = azure_api.StorageAPI()
        azureAPI = StorageAPI()

        res1 = azureAPI.authenticate('blob', 
                    azure_key.getkey('blob', 'account', ),
                    azure_key.getkey('blob', 'key', ),
                    )
        container = azure_key.getkey('blob', 'container', )

        print('authenticate:', res1, )

        if (res1 == True):

            inpPath = '_photos/'
            inpFile = '_photo_cv.jpg'
            res = azureAPI.blob_put(container=container, inpPath=inpPath, inpFile=inpFile, blobFile='', )
            print('blob_put:', res, )

            res = azureAPI.blob_dir(container=container, )
            if (res != False):
                for f in res:
                    print('blob_dir:', f, )

            res = azureAPI.blob_get(container=container, blobFile=inpFile, outPath='', outFile='temp_blob.jpg', )
            print('blob_get:', res, )


