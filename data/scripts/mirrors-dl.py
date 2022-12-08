#!/usr/bin/env python3
# https://mirrors.edge.kernel.org/archlinux/iso/latest/arch/
# https://mirrors.edge.kernel.org/archlinux/iso/latest/
# https://mirrors.edge.kernel.org/alpine/latest-stable/releases/x86_64/netboot/
# https://mirrors.edge.kernel.org/archlinux/iso/latest/archlinux-2022.12.01-x86_64.iso

from pathlib import Path
from urllib.parse import urlparse, urlsplit

import bs4
import click
import requests


def is_dir(a):
    if a.endswith('/'):
        return True
    else:
        return False


def is_parent(a):
    if a == '../':
        return True 
    return False


def find(url):
    """
    Find all urls
    """
    page = requests.get(url).text 

    dirs = bs4.BeautifulSoup(page, "html.parser").find_all("a", href=True)

    for a in dirs:
        if is_parent(a['href']):
            continue
        if is_dir(a['href']):
            # TODO: implement depth
            find(url + a["href"])
        else:
            yield url + a["href"]


def fetch(url, dest, base_url):
    if not url:
        raise Exception("Missing url.")

    if not base_url:
        raise Exception("Missing base_url.")

    if not dest:
        raise Exception("Missing destination path.")

    if not isinstance(dest, Path):
        raise Exception("dest should be `pathlib.Path` instance.")

    filename = Path(urlsplit(url).path).relative_to(Path(urlsplit(base_url).path).parent)
    dest.joinpath(filename.parent).mkdir(parents=True,  exist_ok=True)

    if dest.joinpath(filename).exists():
        return 

    response = requests.get(url, stream=True)

    with open(dest.joinpath(filename), "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return 


class URL(click.ParamType):

    name = "url"

    def convert(self, value, param, ctx):
        check = urlparse(value)
        if all((check.scheme in ("http", "https"), check.netloc)):
            return check
        self.fail(f"{value!r} is not valid url", param, ctx)


@click.command()
@click.argument(
    "origin", 
    nargs=1,
    metavar='<URL>',
    type=URL())
@click.option(
    "-r", 
    "--recursive", 
    is_flag=True, 
    help="Turn on recursive retrieving.")
@click.option(
    "-d", 
    "--dest",
    help="The default is network location from " 
    "`urllib.parse.urlparse.netloc`.",
    type=click.Path())
@click.option(
    "-p", "--prefix", 
    type=click.STRING, 
    help="`prefix` is the directory where all other "
    "files and subdirectories will be saved to, i.e. "
    "the top of the retrieval tree. The default is the "
    "top directory from `urllib.parse.urlparse.path`, "
    "i.e. www.domain.name/top/sub/...")
def download(origin, recursive, dest, prefix):
    """Download file(s)."""

    # TODO: Implement the "--skip-prefix" option for cases that were 
    # downloaded from root tree. In that case, it makes no sense 
    # to keep the "--prefix" option.

    if not dest:
        dest = Path(origin.netloc)

    if not prefix:
        # index -1 get /, -2 get /foo, -3 get /foo/bar ...
        prefix = Path(origin.path).parents[-2]
    # prefix.name transform /foo -> foo/
    dest = Path(dest).joinpath(prefix.name) 

    base_url = origin.geturl()

    if recursive:
        for url in find(base_url):
            fetch(url, dest=dest, base_url=base_url)
        return
    
    if Path(origin.path).suffix:
        suffix = Path(origin.path).suffix
        dest = dest.with_suffix(suffix)
    
    fetch(origin.geturl(), dest=dest, base_url=base_url)


def main():
    download()


if __name__ == '__main__':
    main()
