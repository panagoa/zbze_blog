"""
Модуль для извлечения описаний классов и функций из кода.
"""

from typing import Union

import astroid


def get_docstring(node: Union[astroid.FunctionDef, astroid.ClassDef, astroid.Module]):
    """Возвращает документацию для функции или класса."""
    doc_node = node.doc_node
    return doc_node.value if doc_node else None


def extract_module_docstring(node: astroid.Module):
    """Возвращает документацию для модуля."""
    return get_docstring(node)


def describe_import(node: astroid.Import):
    """Описывает стандартный импорт."""

    imports = []
    for name, alias in node.names:
        if alias:
            imports.append(f"{name} as {alias}")
        else:
            imports.append(name)

    return {
        "type": "Import",
        "names": imports,
    }


def describe_import_from(node: astroid.ImportFrom):
    """Описывает импорт из другого модуля."""
    imports = []

    for name, alias in node.names:
        if alias:
            imports.append(f"{name} as {alias}")
        else:
            imports.append(name)

    return {
        "type": "ImportFrom",
        "module": node.modname,
        "names": imports,
    }


def describe_class(node: astroid.ClassDef):
    """Описывает класс, его методы, атрибуты, документацию и наследование."""
    class_description = {
        "name": node.name,
        "docstring": get_docstring(node),
        "base_classes": [base.as_string() for base in node.bases],
        "methods": [],
        "attributes": [],
    }

    for child in node.get_children():
        if isinstance(child, astroid.FunctionDef):
            method_info = {"name": child.name, "docstring": get_docstring(child), "signature": get_signature(child)}
            class_description["methods"].append(method_info)
        elif isinstance(child, astroid.Assign):
            for target in child.targets:
                if isinstance(target, astroid.AssignName):
                    class_description["attributes"].append(target.name)

    return class_description


def get_signature(node: Union[astroid.FunctionDef, astroid.AsyncFunctionDef]):
    """Возвращает строку с сигнатурой функции или метода."""
    params = [arg.name for arg in node.args.args]
    return_type = node.returns.as_string() if node.returns else None
    return f"{node.name}({', '.join(params)}) -> {return_type}" if return_type else f"{node.name}({', '.join(params)})"


def describe_function(node: Union[astroid.FunctionDef, astroid.AsyncFunctionDef]):
    """Описывает функцию или метод с декораторами, документацией и сигнатурой."""
    return {
        "name": node.name,
        "signature": get_signature(node),
        "docstring": get_docstring(node),
        "decorators": get_decorators_from_node(node),
    }


def get_decorators_from_node(node: Union[astroid.FunctionDef, astroid.AsyncFunctionDef]):
    """Извлекает декораторы из узла."""
    decorators = []
    if hasattr(node, "decorators") and node.decorators is not None:
        for decorator in node.decorators.nodes:
            decorators.append(decorator.as_string())
    return decorators


def extract_descriptions(code):
    """Извлекает описания классов и функций из кода."""

    tree = astroid.parse(code)
    imports = []
    globals = []
    classes = []
    functions = []

    for node in tree.body:
        if isinstance(node, astroid.Import):
            imports.append(describe_import(node))
        if isinstance(node, astroid.ImportFrom):
            imports.append(describe_import_from(node))
        if isinstance(node, astroid.Assign):
            for target in node.targets:
                if isinstance(target, astroid.AssignName):
                    globals.append((target.name, node.value.as_string()))
        if isinstance(node, astroid.ClassDef):
            classes.append(describe_class(node))
        if isinstance(node, (astroid.FunctionDef, astroid.AsyncFunctionDef)):
            functions.append(describe_function(node))

    descriptions = {
        "module_docstring": extract_module_docstring(tree),
        "imports": imports,
        "globals": globals,
        "classes": classes,
        "functions": functions,
    }

    return descriptions
