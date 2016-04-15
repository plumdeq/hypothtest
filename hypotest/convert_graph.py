# coding: utf8
"""
Convert graph for graph visualization packages

:author: Asan Agibetov

"""


def convert_visjs(H):
    """
    (hypograph) -> (nodes_vis_js, edges_vis_js)

    """
    # dict1(**dict2) will create a new dictionary with values updated from dict2
    nodes_vis_js = (dict(id=n, **vis_js_key_names(d))
                    for (n, d) in H.nodes_iter(data=True))

    # python does not like dict(from=1), i.e., from as a key
    edges_vis_js = (dict([("from", f), ("to", t)], **d.copy())
                    for (f, t, d) in H.edges_iter(data=True))

    return (nodes_vis_js, edges_vis_js)


def vis_js_key_names(d):
    """
    dict -> dict

    Convert key names for vis_js default key names, i.e. "value" for the size of
    the node

    mydict[new_key] = mydict.pop(old_key) | change key name

    """
    d["value"] = d.pop("computed importance factor")
    return d.copy()
