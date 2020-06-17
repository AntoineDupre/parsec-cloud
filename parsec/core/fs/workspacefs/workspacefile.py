# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPLv3 2019 Scille SAS

import os

_FILE_SYNC_ATTRS = {
    "closed",
    "encoding",
    "errors",
    "fileno",
    "isatty",
    "newlines",
    "readable",
    "seekable",
    "writable",
    # not defined in *IOBase:
    "buffer",
    "raw",
    "line_buffering",
    "closefd",
    "name",
    "mode",
    "getvalue",
    "getbuffer",
}

_FILE_ASYNC_METHODS = {
    "flush",
    "read",
    "read1",
    "readall",
    "readinto",
    "readline",
    "readlines",
    "seek",
    "tell",
    "truncate",
    "write",
    "writelines",
    # not defined in *IOBase:
    "readinto1",
    "peek",
}


class WorkspaceFile:
    def __init__(self, fd, transactions):
        self._fd = fd
        self._open = True
        self._offset = 0
        self._transactions = transactions

    def __aiter__(self):
        return self

    async def __aenter__(self):
        self._open = True

    async def __aexit__(self, *args):
        self._open = False
        await self.close()

    async def close(self):
        await self._transactions.fd_close(self._fd)

    def closed(self):
        return self._open is False

    def tell(self):
        return self._offset

    async def seek(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self._offset = offset
        if whence == os.SEEK_CUR:
            self._offset += offset
        if whence == os.SEEK_END:
            info = await self._transactions.fd_info(self._fd)
            self._offset = info["size"] + offset
        return self._offset

    async def test_file_stats(self):
        stats = await self._transactions.fd_info(self._fd)
        return stats

    async def readline(self, size=-1):
        raise NotImplementedError

    async def read(self):
        raise NotImplementedError

    async def __anext__(self):
        return await self.readline()

    async def write(self, data):
        self._offset += await self._transactions.write(self._fd, data, self._offset)
