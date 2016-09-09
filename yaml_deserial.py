from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class YamlLoader:

    @staticmethod
    def read(afile):
        with open(afile, 'r') as stream:
            data = load(stream, Loader=Loader)
        return data
