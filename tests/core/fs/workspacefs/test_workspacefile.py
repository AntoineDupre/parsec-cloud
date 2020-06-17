# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPLv3 2019 Scille SAS

import pytest
import trio
import io


@pytest.fixture
@pytest.mark.trio
async def trio_file(tmp_path):
    d = tmp_path / "foo"
    d.mkdir()
    p = d / "baz"
    p.write_text("test")
    p.write_text("test2")
    p.write_text(
        """longtest1longtest1longtest1longtest1longtest1longtest1s
    t1longtest1longtest1longtest1longtest1longtest1longtest1longtest1longtest1lo
    ngtest1longtest1longtest1longtest1longtest1longtest1
    longtest1longtest1longtest1longtest1lon
    gtest1longtest1longtest1longtest1longtest1longtest1longtest1longte
    st1longtest1longtest1longtest1"""
    )
    return p


@pytest.mark.trio
async def test_open(alice_workspace, trio_file):

    f = await alice_workspace.open_file("/foo/bar", "r")
    f2 = await alice_workspace.open_file("/foo/bar", "r")
    triof = await trio.open_file(trio_file, "r")
    triof2 = await trio.open_file(trio_file, "r")
    assert (triof != triof2) == (f != f2)
    assert f._fd == 1 and f2._fd == 2


@pytest.mark.trio
async def test_read(alice_workspace, trio_file):
    print("\n")
    # f = await alice_workspace.open_file("/foo/bar", "r")
    triof = await trio.open_file(trio_file, "r")
    triolines = ""
    # lines = ""
    # async for line in f:
    #     lines += line
    async for line in triof:
        triolines += line
        print("newline = " + line + "\n")
    # print(lines)


@pytest.mark.trio
async def test_seek(alice_workspace, trio_file):

    f = await alice_workspace.open_file("/foo/bar", "r")
    triof = await trio.open_file(trio_file, "r")
    # test seek end
    await f.seek(100, io.SEEK_END)
    await triof.seek(0, io.SEEK_END)
    print("\n ", await f.test_file_stats())
