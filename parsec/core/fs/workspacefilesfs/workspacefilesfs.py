# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPLv3 2019 Scille SAS

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


class WorkspaceFilesFS:
    def __init__(self, fd, transactions):
        self._fd = fd
        self._open = None
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

    async def __anext__(self):
        return await self._transactions.fd_read(self._fd, 5, 0)
