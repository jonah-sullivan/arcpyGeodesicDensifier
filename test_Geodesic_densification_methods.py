import arcpy
import math
from geographiclib.geodesic import Geodesic

# generic parameters
canberra = {'x':149, 'y':-35}
perth = {'x':115, 'y':-32}
ds = 100000  # maximum segment length(m)

# arcpy methods
canberraPointGeom = arcpy.PointGeometry(arcpy.Point(canberra['x'], canberra['y']), arcpy.SpatialReference(4326))
perthPointGeom = arcpy.PointGeometry(arcpy.Point(perth['x'], perth['y']), arcpy.SpatialReference(4326))
angle, distance = canberraPointGeom.angleAndDistanceTo(perthPointGeom, "GEODESIC")
waypoint = canberraPointGeom
print("arcpy distance:         " + str(distance))

# geographiclib methods
geod = Geodesic.WGS84
l = geod.InverseLine(canberra['y'], canberra['x'],
                     perth['y'], perth['x'])
print("geographiclib distance: " + str(l.s13))

# generic parameters
n = int(math.ceil(distance / ds))  # number of segments
seglen = distance / n

# loop through segments
for i in range(n + 1):
    if i == 0:
        print(", ".join(["method", "segmentNo", "azimuth", "distance", "long", "lat"]))
    else:
        # arcpy method
        fullAng, fullDist = waypoint.angleAndDistanceTo(perthPointGeom, "GEODESIC")
        newWaypoint = waypoint.pointFromAngleAndDistance(fullAng, seglen, "GEODESIC")
        segAng, segDist = waypoint.angleAndDistanceTo(newWaypoint, "GEODESIC")
        waypoint = newWaypoint

        arcpy_output = str(int(i)).zfill(2) + " " + \
                       str(segAng).ljust(18,'0') + " " + \
                       str(str(int(min(seglen * i, distance)))).zfill(7) + " " + \
                       str(newWaypoint.extent.XMax).ljust(19,'0') + " " + \
                       str(newWaypoint.extent.YMax).ljust(19,'0')

        print("arcpy " + arcpy_output)

        # geographiclib method
        g = l.Position(min(seglen * i, l.s13))
        
        geographiclib_output = str(int(i)).zfill(2) + " " + \
                               str(g['azi2']).ljust(18,'0') + " " + \
                               str(int(min(seglen * i, l.s13))).zfill(7) + " " + \
                               str(g['lon2']).ljust(19,'0') + " " +\
                               str(g['lat2']).ljust(19,'0')
        
        print("geogr " + geographiclib_output)
        print(" ")
