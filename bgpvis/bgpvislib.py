"""
base lib for dump file handling

Hynek Los v0.1
"""

import logging
import os
from os import path
from logging import StreamHandler
import requests
from requests import get
from mrtparse import *




logger = logging.getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(logging.DEBUG)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class BGPDumpData(object):
    """dump file class"""
    RIPE_FILENAME = "ripebgp.mrt"

    def downloadMRT(self,url, fileName):
        with open(fileName, "wb") as file:
            response = get(url)
            file.write(response.content)

    def getRipeDump(self):
        """fetch ripe data dump"""
        tmp = "http://data.ris.ripe.net/rrc00/2020.05/bview.20200521.0800.gz"
        logger.debug(__name__+":starting download "+tmp)
        self.downloadMRT(url=tmp,fileName=ROOT_DIR + os.sep + self.RIPE_FILENAME)
        logger.debug(__name__ + ":finished download " + tmp)

    def __init__(self,cached=True):
        """init data"""
        logger.debug(__name__+":constructor")
        if path.exists(ROOT_DIR+os.sep+self.RIPE_FILENAME) == False or  cached==False:
            if path.exists(ROOT_DIR + os.sep + self.RIPE_FILENAME):
                os.remove(ROOT_DIR+os.sep+self.RIPE_FILENAME)
            self.getRipeDump()

        #doublecheck:
        if path.exists(ROOT_DIR + os.sep + self.RIPE_FILENAME) == False:
            logger.error(__name__+": sory, i have no "+ROOT_DIR + os.sep + self.RIPE_FILENAME)
            raise Exception(__name__+": sory, i have no "+ROOT_DIR + os.sep + self.RIPE_FILENAME)
        else:
            logger.info(__name__+ROOT_DIR + os.sep + self.RIPE_FILENAME+" found.. proceeding with init")


    def mrtInfo(self):
        """print mrt file summary"""
        mr = Reader(ROOT_DIR+os.sep+self.RIPE_FILENAME)
        c=0
        for row in mr:
            mrt = row.mrt
            logger.info(f"{__class__}: {str(mrt.type)}")
            if c>100:
                break
            c+=1
            if mrt.err == MRT_ERR_C['MRT Data Error']:
                logger.info("mrtInfo: MRT Data Error "+mrt.type)
            if mrt.type == MRT_T['TABLE_DUMP_V2']:

                if mrt.subtype == TD_V2_ST['PEER_INDEX_TABLE']:
                    logger.info(f"mrtInfo: {mrt.peer.collector}")




if __name__ == '__main__':
    bg = BGPDumpData()
    bg.mrtInfo()
