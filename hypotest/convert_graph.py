# coding: utf8
"""
Convert graph for graph visualization packages

:author: Asan Agibetov

"""
import hypotest


def convert_visjs(H):
    """
    (hypograph) -> (nodes_vis_js, edges_vis_js)

    """
    # make sure that no mutable operation is perfomed on the original graph
    H = H.copy()
    # recompute colors
    H = compute_colors(H)

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


def from_vis_js_key_names(d):
    """
    dict -> dict

    Convert key names from vis_js default key names, i.e. "value" for the size
    of the node. Delete id key name, otherwise it will be duplicated

    mydict[new_key] = mydict.pop(old_key) | change key name

    """
    d["computed importance factor"] = d.pop("value")
    d_copy = d.copy()
    d_copy.pop('id', None)

    return d_copy


def compute_colors(H):
    """
    hypograph -> hypograph with colors based on evidenced

    not evidenced - "color: red"
    evidenced - "color: green"

    """
    clr_unevidenced = 'rgba(194, 91, 91'
    clr_evidenced = 'rgba(91, 194, 92'

    for (n, d) in H.nodes_iter(data=True):
        if d['evidenced'] == 1:
            d['color'] = clr_evidenced
        else:
            d['color'] = clr_unevidenced

        # opaque if endpoints, semi-transparent otherwise
        if d['causal_endpoint'] == 1:
            d['color'] = ''.join((d['color'], ', 1)'))
        else:
            d['color'] = ''.join((d['color'], ', 0.5)'))

    return H


def convert_from_visjs_nodes(nodes):
    """
    ([node_visjs_dict, ...]) -> ([node_id, dict])

    """
    return ([d['id'], dict(**from_vis_js_key_names(d))]
            for d in nodes)


def convert_from_visjs_graph(nodes):
    """
    ([node_visjs_dict, ...]) -> hypothgraph

    """
    H1 = hypotest.H.copy()

    nodes = convert_from_visjs_nodes(nodes)

    # update nodes of the hypothgraph
    H1.add_nodes_from(nodes)

    return H1
