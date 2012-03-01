from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from leam.luc import lucMessageFactory as _



class ILUCScenario(Interface):
    """LEAM Land Use Change (LUC) Scenario"""

    # -*- schema definition goes here -*-
    cmdline = schema.TextLine(
        title=_(u"Command line to begin execution after checkout of repository."),
        required=True,
        description=_(u"blah"),
    )
#
    repository = schema.TextLine(
        title=_(u"Code Repository"),
        required=True,
        description=_(u"The subversion repository containing necessary run time files."),
    )
#
    end_time = schema.Date(
        title=_(u"End Time"),
        required=False,
        description=_(u"When the model completed."),
    )
#
    start_time = schema.Date(
        title=_(u"Start Time"),
        required=False,
        description=_(u"When the model began execution."),
    )
#
    runstatus = schema.TextLine(
        title=_(u"Run Status"),
        required=True,
        description=_(u"Provide the current run state of the scenario."),
    )
#
    roads = schema.Object(
        title=_(u"Additional Roads"),
        required=False,
        description=_(u"Select a GIS layer that contains any roads not included in the TDM network."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    transit = schema.Object(
        title=_(u"Transit Networks"),
        required=False,
        description=_(u"Select one or more GIS layers containing regional or local transite networks."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    tdm = schema.Object(
        title=_(u"Travel Demand Model Transportation Network"),
        required=True,
        description=_(u"Select a transportation network that has been generated from a travel demand model."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    nogrowth = schema.Object(
        title=_(u"No Growth Maps"),
        required=False,
        description=_(u"Select one or more GIS layers.  These areas will be protected from model development."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    empcenters = schema.Object(
        title=_(u"Employment Centers"),
        required=True,
        description=_(u"Select a GIS layer containing employeers and employmment centers."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    popcenters = schema.Object(
        title=_(u"City and Population Centers"),
        required=True,
        description=_(u"Select the GIS layer with city centers."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    dem = schema.Object(
        title=_(u"Digital Elevation Map"),
        required=True,
        description=_(u"Select a GIS layer that provides regional elevation."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    landuse = schema.Object(
        title=_(u"Initial Land Use Map"),
        required=True,
        description=_(u"Provide an initial land use map for the scenario.  Unused if a Starting Scenario is provided."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    syear = schema.Int(
        title=_(u"Starting Year"),
        required=True,
        description=_(u"Enter the starting year of the scenario."),
    )
#
    starting_scenario = schema.Object(
        title=_(u"Starting Scenario"),
        required=False,
        description=_(u"Select existing scenario if the new scenario will build upon previous model results."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    subregions = schema.Object(
        title=_(u"Sub-Regional Projections"),
        required=False,
        description=_(u"Add as many subregional projections as needed."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    region = schema.Object(
        title=_(u"Regional Projection"),
        required=True,
        description=_(u"Identify the study area and population and employment projections."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
