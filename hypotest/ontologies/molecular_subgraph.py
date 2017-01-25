#!/usr/bin/env python
# -*- coding: utf-8 -*-

# # Molecular subgraph used in the paper
#
from rdflib.extras.infixowl import (
        Ontology, Class, Property, CastClass, some
    )
from rdflib import Namespace, Graph, OWL, Literal
from rdflib.namespace import NamespaceManager

ns = Namespace('http://plumdeq.xyz/ontologies/hypothesis/')
ns_manager = NamespaceManager(Graph())
ns_manager.bind('hypo', ns, override=False)
ns_manager.bind('owl', OWL, override=False)
g = Graph()
g.namespace_manager = ns_manager


ontology = Ontology(
        ns.identifier,
        comment=Literal('defined by: Asan Agibetov, Marta Ondresik, Ernesto Jimenez-Ruiz'),
        graph=g)


# ## Main classes
#
# con = Class(ns.Continuant, graph=g, comment=Literal('Material entity. Examples: cells, molecules, joints'))
occ = Class(ns.Occurent, graph=g, comment=Literal('Occuring processes, which start and end at some point'))
condition = Class(ns.Condition, graph=g, comment=Literal('Medical condition. Could be a pathology or a disorder'))

# ##  Properties

# Main properties, such as `capable of`, `negatively regulates`
# capable_of = Property(ns.capable_of, graph=g, domain=[occ], range=[occ])
negatively_regulates = Property(ns.negatively_regulates, graph=g, domain=[occ], range=[occ])
positively_regulates = Property(ns.positively_regulates, graph=g, domain=[occ], range=[occ])
# reduces_levels_of = Property(ns.reduces_levels_of, graph=g, domain=[occ], range=[con])
# increases_levels_of = Property(ns.increases_levels_of, graph=g, domain=[occ], range=[con])
# inhibits = Property(ns.inhibits, graph=g, domain=[occ], range=[occ])
# activates = Property(ns.activates, graph=g, domain=[occ], range=[occ])
results_in = Property(ns.results_in, graph=g, domain=[occ], range=[occ])
causes = Property(ns.causes, graph=g, domain=[occ], range=[occ])

# ## Atomic continuants
#
# We model basic classes in our hypothesis ontology, which represent bio
# macro-molecules, biomolecules and cells in the cartillage
#
# * chondrocytes (cells)
# * cytokines (biomolecules), pro-inflammatory guys
# * tnf-alpha (biomolecule), mmp13 (enzyme), adamt (enzyme) bad guys
# * collagen, proteoglycan (macro-molecules) good guys
# chondrocytes = Class(
#         ns.Chondrocytes,
#         graph=g,
#         subClassOf=[con],
#         comment=Literal('Chondrocytes are the ontly cells in the knee cartilage')
#     )
#
# collagen = Class(
#         ns.Collagen_type_II,
#         graph=g,
#         subClassOf=[con],
#         comment=Literal('Collagen type II, macromolecule, together with Proteoglycans, are the main building blocks of the cartilage.')
#     )
#
# proteoglycan = Class(
#         ns.Proteoglycan,
#         graph=g,
#         subClassOf=[con],
#         comment=Literal('A macromolecule, together with Collagen are the main building blocks of the cartilage')
#     )
#
# tnf_alpha = Class(
#         ns.TNF_alpha,
#         graph=g,
#         subClassOf=[con],
#         comment=Literal('A biomolecule which is capable of inhibiting collagen and protaeglycan production, the latter are necessary for the molecular stability of the cartilage')
#     )
#
# mmp13 = Class(
#         ns.MMP13,
#         graph=g,
#         subClassOf=[con],
#         comment=Literal('Enzyme which is capable of catalyzing chondrocytes catabolic activity, i.e., break down of collagen and proteoglycans')
#     )
#
# aggrecanases = Class(
#         ns.Aggrecanases,
#         graph=g,
#         subClassOf=[con],
#         comment=Literal('Enzyme which is capable of catalyzing chondrocytes catabolic activity, i.e., break down of collagen and proteoglycans')
#     )

# ## Atomic occurrents
#
# Atomic occurrents include anabolic/catabolic activities of continuants,
# production of certain molecules and destruction or disassembly of certain
# molecules

# ## Processes linked with `chondrocytes`
chondro_anabolic = Class(
        ns.Chondrocytes_anabolic_activity,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Chondrocytes anabolic activity is the process of construction of molecules from smaller units')
    )

chondro_catabolic = Class(
        ns.Chondrocytes_catabolic_activity,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Chondrocytes catabolic activity is the process of separation of molecules. Opposite of chondrocytes anabolism')
    )

# chondro_apoptosis = Class(
#         ns.Chondrocytes_apoptosis,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Chondrocytes apoptosis is the process where the chondrocytes, cells, are dying')
#     )
#
# chondro_hyper = Class(
#         ns.Chondrocytes_hypertrophy,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Increase in the volume of an organ or tissue due ot the enlargement of its component cells')
#     )

# processes linked with production of molecules
collagen_production = Class(ns.Collagen_production, graph=g, subClassOf=[occ])
proteoglycan_production = Class(ns.Proteoglycan_production, graph=g, subClassOf=[occ])
# tnf_production = Class(ns.TNF_alpha_production, graph=g, subClassOf=[occ])
mmp13_production = Class(ns.MMP13_production, graph=g, subClassOf=[occ])
aggrecanases_production = Class(ns.Aggrecanases_production, graph=g, subClassOf=[occ])

# processes linked with catabolism of molecules
collagen_loss = Class(
        ns.Loss_of_collagen,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Loss of collagen molecules, a process which reduces the levels of collagen molecules')
    )

proteoglycan_loss = Class(
        ns.Loss_of_proteoglycan,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Loss of proteoglycan molecules, a process which reduces the levels of proteoglycan molecules')
    )

# processes which are hidden, our system should suggest them
tnf_overproduction = Class(ns.TNF_alpha_overproduction, graph=g, subClassOf=[occ])

# ## Processes outside cellular scale
#
# mechanical_loading = Class(
#         ns.Mechanical_loading,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Mechanical loading of the cartilage, environmental factor')
#     )
#
# # ## Processes which involve cartilage on organ scale
# #
# cartilage_calcification = Class(
#         ns.Cartilage_calcification,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Calcification is the accumulation of calcium salts in a body tissue, causing it to harden')
#     )
#
# decrease_cartilage_elasticity = Class(
#         ns.Decrease_of_cartilage_elasticity,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Cartilage is becoming too stiff and starts losing its elasticity properties')
#     )

biochemical_imbalance = Class(
        ns.Biochemical_imbalance,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Biochemical imbalance in the cartilage')
    )

# water_content_increase = Class(
#         ns.Water_content_increase_in_cartilage,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Water content increase in cartilage process')
#     )
#
# # ## Organ scale processes
# #
# diminution_load_bearing = Class(
#         ns.Diminution_of_load_bearing_capacity_of_cartilage,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Diminution of load bearing capacity of cartilage')
#     )
#
# bone_erosion = Class(
#         ns.Bone_erosion,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Reduction of the surface of a bone')
#     )
#
# osteophyte_formation = Class(
#         ns.Osteophyte_formation,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Osteophytes, or bone spurs, are bony projections that form along joint margins')
#     )
#
# joint_deformation = Class(
#         ns.Joint_deformation,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Joint deformation is a general process of anatomical deformation of soft and bony tissues which surround the joint')
#     )

cartilage_degeneration = Class(
        ns.Cartilage_degeneration,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Cartilage degeneration is a generic process where the surface of cartilage is being degenerated')
    )

# joint_functional_impairment = Class(
#         ns.Joint_functional_impairment,
#         graph=g,
#         subClassOf=[occ],
#         comment=Literal('Reduction of joint movement range')
#     )

synovial_inflammation = Class(
        ns.Synovial_inflammation,
        graph=g,
        subClassOf=[occ],
        comment=Literal('Inflammation in a synovial joint')
    )


# ## Conditions, pathologies and disorders
#

# knee_effusion = Class(
#         ns.Swelling_of_knee,
#         graph=g,
#         subClassOf=[condition],
#         comment=Literal('Knee effusion, or water on the knee, or knee swelling is a condition')
#     )
#
# ligamentous_laxity = Class(
#         ns.Ligamentous_laxity,
#         graph=g,
#         subClassOf=[condition],
#         comment=Literal('Loose ligaments, maybe genetic. Ligamentous laxity if the cause of chronic body pain. ICD-10:M24.2')
#     )
#
# knee_pain = Class(
#         ns.Knee_pain,
#         graph=g,
#         subClassOf=[condition],
#         comment=Literal('Knee pain, chronic or acute')
#     )
#
# meniscal_tear = Class(
#         ns.Meniscal_tear,
#         graph=g,
#         subClassOf=[condition],
#         comment=Literal('Tear of meniscus, meniscus breakdown')
#     )

# ## Causal relations via restrictions
#
# * anabolism of chondrocytes is good for collagen, proteoglycans production
# * catabolism of chondrocytes is good for tnf-alpha, mmp13, adamt production
# * tnf_alpha inihibts collagen/proteoglycan production
# * mmp13 digests available collagen
# * adamt digest available proteoglyecan

# assigning new parents only adds them, previous parents are not deleted
chondro_anabolic.subClassOf = [
        (positively_regulates | some | collagen_production),
        (positively_regulates | some | proteoglycan_production)
    ]

chondro_catabolic.subClassOf = [
        # (positively_regulates | some | tnf_production),
        (positively_regulates | some | mmp13_production),
        (positively_regulates | some | aggrecanases_production),
        (results_in | some | proteoglycan_loss),
        (results_in | some | collagen_loss)
    ]

# chondro_hyper.subClassOf = [
#         (positively_regulates | some | mmp13_production),
#         (positively_regulates | some | aggrecanases_production),
#         (negatively_regulates | some | chondro_anabolic),
#         (results_in | some | cartilage_calcification),
#         (results_in | some | osteophyte_formation)
#     ]

tnf_overproduction.subClassOf = [
        (negatively_regulates | some | chondro_anabolic),
        (positively_regulates | some | chondro_catabolic),
        (negatively_regulates | some | proteoglycan_production),
        (negatively_regulates | some | collagen_production),
        (results_in | some | proteoglycan_loss),
        (results_in | some | collagen_loss)
    ]

# tnf_production.subClassOf = [
#         (increases_levels_of | some | tnf_alpha)
#     ]

mmp13_production.subClassOf = [
        (results_in | some | collagen_loss)
    ]

aggrecanases_production.subClassOf = [
        (results_in | some | proteoglycan_loss)
    ]

synovial_inflammation.subClassOf = [
        (results_in | some | tnf_overproduction),
        # (results_in | some | knee_pain),
        # (results_in | some | joint_deformation)
    ]

# chondro_apoptosis.subClassOf = [
#         (results_in | some | collagen_loss),
#         (results_in | some | proteoglycan_loss)
#     ]

# ## Causal relations outside of the cellular level
#
# mechanical_loading.subClassOf = [
#         (positively_regulates | some | chondro_catabolic),
#         (positively_regulates | some | chondro_anabolic),
#         (results_in | some | chondro_apoptosis),
#         (results_in | some | cartilage_degeneration),
#         (results_in | some | meniscal_tear)
#     ]

collagen_loss.subClassOf = [
        # (results_in | some | decrease_cartilage_elasticity),
        (results_in | some | biochemical_imbalance)
    ]

proteoglycan_loss.subClassOf = [
        # (results_in | some | decrease_cartilage_elasticity),
        (results_in | some | biochemical_imbalance)
    ]

biochemical_imbalance.subClassOf = [
        # (results_in | some | water_content_increase),
        # (results_in | some | diminution_load_bearing)
        (results_in | some | cartilage_degeneration)
    ]

# water_content_increase.subClassOf = [
#         (results_in | some | diminution_load_bearing)
#     ]
#
# cartilage_calcification.subClassOf = [
#         (results_in | some | diminution_load_bearing)
#     ]
#
# decrease_cartilage_elasticity.subClassOf = [
#         (results_in | some | diminution_load_bearing)
#     ]

# ## Behavioral scale causal relations
#
# diminution_load_bearing.subClassOf = [
#         (results_in | some | cartilage_degeneration),
#         (results_in | some | bone_erosion)
#     ]
#
# osteophyte_formation.subClassOf = [
#         (results_in | some | joint_deformation),
#         (results_in | some | knee_pain)
#     ]

# cartilage_degeneration.subClassOf = [
#         (results_in | some | joint_functional_impairment),
#         (results_in | some | knee_pain)
#     ]

# ligamentous_laxity.subClassOf = [
#         (results_in | some | joint_deformation),
#         (results_in | some | knee_pain)
#     ]
#
# bone_erosion.subClassOf = [
#         (results_in | some | joint_deformation)
#     ]
#
# joint_deformation.subClassOf = [
#         (results_in | some | joint_functional_impairment)
#     ]
#
# knee_effusion.subClassOf = [
#         (results_in | some | joint_deformation),
#         (results_in | some | joint_functional_impairment)
#     ]
#
# knee_pain.subClassOf = [
#         (results_in | some | joint_functional_impairment)
#     ]

# ## Cyclic causality relations
#
cartilage_degeneration.subClassOf = [
        (results_in | some | synovial_inflammation),
        # (results_in | some | meniscal_tear)
    ]

# meniscal_tear.subClassOf = [
#         (results_in | some | cartilage_degeneration),
#         (results_in | some | joint_functional_impairment),
#         (results_in | some | knee_pain)
#     ]
