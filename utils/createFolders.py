import os, sys
import optparse

from leamsite import LEAMsite


def main():

    usage = "usage: %prog [options] <site URL>"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-t", "--topfolder", default="",
        help="create a toplevel folder")
    parser.add_option("-u", "--user", default="admin",
        help="Plone user")
    parser.add_option("-p", "--password", default="leam4z",
        help="Plone user's password")

    (opts, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("the URL to the Plone site is required")

    url = args[0]
    site = LEAMsite(url, user=opts.user, passwd=opts.password)
    if site.error:
        parser.error("the URL is not a valid site")

    if opts.topfolder:
        url = site.createFolder(opts.topfolder, url)

    projections = site.createFolder("projections", url)
    site.editFolder(projections, 
        title="Population and Employment Projections",
        description="""Enter population and employment projection in this folder.  The projection may contains zones, population and employment densities."""
    )

    subregional = site.createFolder("subregional", url)
    site.editFolder(subregional,
        title="Subregional Maps",
        description="""Subregional maps identify different zones used within the model.  This maps can be used as part of a projection or within impact models.  """
    )

    transportation = site.createFolder("transportation", url)
    site.editFolder(transportation,
        title="Transportation Networks",
        description="""Transportation networks require two fields, FCLASS and MINSPEED.  FCLASS is the function class of the road.  MINSPEED represents the calculated speed at peak traffic times.  """
    )
    
    nogrowth = site.createFolder("nogrowth", url)
    site.editFolder(nogrowth,
        title = "No Growth Maps",
        description = """No growth layers are used to remove areas from development.  No special fields are required for this layer.  Any areas identified in "no growth" layers will be removed from the model.  """
    )

    specials = site.createFolder("specials", url)
    site.editFolder(specials,
        title = "Special Drivers",
        description="""Special drivers provides a mechanism for directly modifying the probability maps. All special drivers must contain fields.  """
    )

    landuse = site.createFolder("landuse", url)
    site.editFolder(landuse,
        title="Land Use Maps",
        description="""Enter initial land use and DEM maps in this folder."""
    )

    attractors = site.createFolder("attractors", url)
    site.editFolder(attractors,
        title="Regional Attractors",
        description="""Enter regional attractors such as cities and employment centers in this folder. The cities layer is a point layer and must have provide the population in field POP.  The employment layer should have the number of employees associated with each employment center in the EMP field.  """
    )


if __name__ == "__main__":
    main()
