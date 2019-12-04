#! /usr/bin/env jython
# Copyright (C) 2011 Sun Ning<classicning@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import sys
import time
import queue
import threading
import logging

JIP_USER_AGENT = 'jip-koalanlp/1.0'
BUF_SIZE = 4096


class DownloadException(Exception):
    pass


def download(url, target, asynchronous=False, close_target=False, quiet=True):
    import requests
    # download file to target (target is a file-like object)

    if asynchronous:
        pool.submit(url, target)
    else:
        try:
            t0 = time.time()
            source = requests.get(url, headers={'User-Agent': JIP_USER_AGENT})
            source.raise_for_status()
            size = source.headers['Content-Length']
            if not quiet:
                logging.info('[Downloading] %s %s bytes to download' % (url, size))
            for buf in source.iter_content(BUF_SIZE):
                target.write(buf)
            source.close()
            if close_target:
                target.close()
            t1 = time.time()
            if not quiet:
                logging.info('[Downloading] Download %s completed in %f secs' % (url, (t1 - t0)))
        except requests.exceptions.RequestException:
            _, e, _ = sys.exc_info()
            raise DownloadException(url, e)


def download_string(url):
    import requests
    try:
        response = requests.get(url, headers={'User-Agent': JIP_USER_AGENT})
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        _, e, _ = sys.exc_info()
        raise DownloadException(url, e)


def wait_until_download_finished():
    pool.join()


class DownloadThreadPool(object):
    def __init__(self, size=3):
        self.queue = queue.Queue()
        self.workers = [threading.Thread(target=self._do_work) for _ in range(size)]
        self.initialized = False

    def init_threads(self):
        for worker in self.workers:
            worker.setDaemon(True)
            worker.start()
        self.initialized = True

    def _do_work(self):
        while True:
            url, target = self.queue.get()
            download(url, target, close_target=True, quiet=False)
            self.queue.task_done()

    def join(self):
        self.queue.join()

    def submit(self, url, target):
        if not self.initialized:
            self.init_threads()
        self.queue.put((url, target))


pool = DownloadThreadPool(3)


__all__ = ['DownloadException', 'download', 'download_string', 'wait_until_download_finished']
