import clang.cindex
from clang.cindex import Index
from clang.cindex import Config

Config.set_compatibility_check(False)
Config.set_library_file("/usr/lib/x86_64-linux-gnu/libclang-9.so")

def print_method_area(node):
    if (node.kind.name == 'FUNCTION_DECL'):
        print("file : {0}".format(node.extent.start.file))
        print("function : {0}".format(node.displayname))
        print(" from line:{0} column:{1}".format(node.extent.start.line, node.extent.start.column))
        print(" to   line:{0} column:{1}".format(node.extent.end.line, node.extent.end.column))
    for child in node.get_children():
        print_method_area(child)

index = Index.create() 
tu = index.parse("test.cpp")
print_method_area(tu.cursor)