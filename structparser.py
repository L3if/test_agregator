import sys
import clang.cindex
import typing
from os import path
clang.cindex.Config.set_library_path('/Library/Developer/CommandLineTools/usr/lib')


def get_cpp_funcs(file_path):
    if path.exists(file_path) and file_path.endswith('.cpp'):
        func_list = []
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_path, args=['-std=c++11'])

        def filter_node_list_by_node_kind(
            nodes: typing.Iterable[clang.cindex.Cursor],
            kinds: list
        ) -> typing.Iterable[clang.cindex.Cursor]:
            result = []

            for i in nodes:
                if i.kind in kinds:
                    result.append(i)

            return result
        all_func = filter_node_list_by_node_kind(translation_unit.cursor.get_children(), [clang.cindex.CursorKind.FUNCTION_DECL])
        for i in all_func:
            if not i.spelling.startswith('operator'):
                func_list.append(i.spelling)
        return func_list
    else:
        print('path ether not exis or it\'s not a repo')
        return None
