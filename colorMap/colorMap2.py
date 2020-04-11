from __future__ import (absolute_import, division, print_function)
import os
os.environ['PROJ_LIB'] = 'D:\ProgramData\Anaconda3\pkgs\proj4-5.2.0-ha925a31_1\Library\share'
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
import pulp
import csv

N = 538
def changeUndToSpace(L):
    for i in range(len(L)):
        if L[i] == '_':
            L[i] = ' '
    return L
def getResultBinary(vote, pop):
    s = 0
    for i in range(len(vote)):
        s += float(vote[i][0]) * pop[i]
    print(s)
    return s
with open('D:\Pycharm\OperationalReseaerch\DataElectionEligible.csv', newline='') as f:
    reader = csv.reader(f)
    pop = list(reader)

with open('D:\Pycharm\OperationalReseaerch\LabelState.csv', newline='') as f:
    reader = csv.reader(f)
    alphalab = list(reader)

with open(r'D:\Pycharm\OperationalReseaerch\binaryvote.csv', newline='') as f:
    reader = csv.reader(f)
    binaryvote = list(reader)

#Initialize variables
p1 = pulp.LpProblem("US Elections 2016", pulp.LpMinimize)
#Initialize variables, Use LpContinuous for R, LpInteger
u = pulp.LpVariable("u", 0, None, pulp.LpContinuous)
v = pulp.LpVariable("v", 0, None, pulp.LpContinuous)
alpha = []
for j in alphalab :
    j = pulp.LpVariable(str(j[0]), 0, None, pulp.LpInteger)
    alpha.append(j)
#Add the objective function
p1 += u - v
#Add constraints
for j in range(len(alphalab)) :
    p1 += v - alpha[j] * 1e6 / float(pop[j][0]) <= 0
    p1 += alpha[j] * 1e6 / float(pop[j][0]) - u <=0
#Add the last equality constraint
    p1 += sum(alpha) == N
#Write LP into a .lp file
p1.writeLP("TP2LP1.lp")
#Solve the LP
#Another solver can be used by inserting it into the parenthesis ex : p1.solve(CPLEX())
p1.solve()
#Print status of the solution
print("Status:", pulp.LpStatus[p1.status])
#Print solution variables
alphares = []
stateID = []

for v in p1.variables():
    alphares.append(v.varValue)
    stateID.append(str(v.name))
    print(v.name, "=", v.varValue)
stateID = stateID[:-2]
alphares = alphares[:-2]
#Objective function value
print("Objective function value = ", pulp.value(p1.objective))
mat = np.array([alphares, stateID])
newstateID = [i[0] for i in alphalab]
print(newstateID)
newalphares = [alphares[i]*1e6/float(pop[i][0]) for i in range(len(alphares))]
for i in range(len(newalphares)):
    print(stateID[i], ':', round(newalphares[i],3))
zipbObj = zip(newstateID, newalphares)
dictOfWords = dict(zipbObj)
print(dictOfWords)
s = getResultBinary(binaryvote, alphares)
print(N/2)
if (s < N/2) :
    print("Winner : Trump")
elif (s > N/2):
    print("Winner : Clinton")
else :
    print("Undecided, need to take more into account")

fig, ax = plt.subplots()

# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# Mercator projection, for Alaska and Hawaii
m_ = Basemap(llcrnrlon=-190,llcrnrlat=20,urcrnrlon=-143,urcrnrlat=46,
            projection='merc',lat_ts=20)  # do not change these numbers

#%% ---------   draw state boundaries  ----------------------------------------
## data from U.S Census Bureau
## http://www.census.gov/geo/www/cob/st2000.html
shp_info = m.readshapefile('D:\ProgramData\Anaconda3\pkgs\proj4-5.2.0-ha925a31_1\Library\share\st99_d00','states',drawbounds=True,
                           linewidth=0.45,color='gray')
shp_info_ = m_.readshapefile('D:\ProgramData\Anaconda3\pkgs\proj4-5.2.0-ha925a31_1\Library\share\st99_d00','states',drawbounds=False)

## population density by state from
## http://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
popdensity = dictOfWords
#%% -------- choose a color for each state based on population density. -------
colors={}
statenames=[]
cmap = plt.cm.plasma # use 'reversed hot' colormap
vmin = min(newalphares ); vmax = max(newalphares) # set range.
norm = Normalize(vmin=vmin, vmax=vmax)
for shapedict in m.states_info:
    statename = shapedict['NAME']
    # skip DC and Puerto Rico.
    if statename not in ['District of Columbia','Puerto Rico']:
        pop = popdensity[statename]
        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        colors[statename] = cmap(np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
    statenames.append(statename)

#%% ---------  cycle through state names, color each one.  --------------------
for nshape,seg in enumerate(m.states):
    # skip DC and Puerto Rico.
    if statenames[nshape] not in ['Puerto Rico', 'District of Columbia']:
        color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)

AREA_1 = 0.005  # exclude small Hawaiian islands that are smaller than AREA_1
AREA_2 = AREA_1 * 30.0  # exclude Alaskan islands that are smaller than AREA_2
AK_SCALE = 0.19  # scale down Alaska to show as a map inset
HI_OFFSET_X = -1900000  # X coordinate offset amount to move Hawaii "beneath" Texas
HI_OFFSET_Y = 250000    # similar to above: Y offset for Hawaii
AK_OFFSET_X = -250000   # X offset for Alaska (These four values are obtained
AK_OFFSET_Y = -750000   # via manual trial and error, thus changing them is not recommended.)

for nshape, shapedict in enumerate(m_.states_info):  # plot Alaska and Hawaii as map insets
    if shapedict['NAME'] in ['Alaska', 'Hawaii']:
        seg = m_.states[int(shapedict['SHAPENUM'] - 1)]
        if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > AREA_1:
            seg = [(x + HI_OFFSET_X, y + HI_OFFSET_Y) for x, y in seg]
            color = rgb2hex(colors[statenames[nshape]])
        elif shapedict['NAME'] == 'Alaska' and float(shapedict['AREA']) > AREA_2:
            seg = [(x*AK_SCALE + AK_OFFSET_X, y*AK_SCALE + AK_OFFSET_Y)\
                   for x, y in seg]
            color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor='gray', linewidth=.45)
        ax.add_patch(poly)

ax.set_title('Number of electors per million of eligible voters - Improved')
ax.annotate('Winner : Donald Trump', (3000000, 90000))
#%% ---------  Plot bounding boxes for Alaska and Hawaii insets  --------------
light_gray = [0.8]*3  # define light gray color RGB
x1,y1 = m_([-190,-183,-180,-180,-175,-171,-171],[29,29,26,26,26,22,20])
x2,y2 = m_([-180,-180,-177],[26,23,20])  # these numbers are fine-tuned manually
m_.plot(x1,y1,color=light_gray,linewidth=0.8)  # do not change them drastically
m_.plot(x2,y2,color=light_gray,linewidth=0.8)

#%% ---------   Show color bar  ---------------------------------------
ax_c = fig.add_axes([0.9, 0.1, 0.02, 0.5])
cb = ColorbarBase(ax_c,cmap=cmap,norm=norm,orientation='vertical',
                  label=r'[Electoral college members / M eligible voters]')

plt.show()