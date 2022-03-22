import pyperclip
from objects.base import spherical_to_cartesian
import json

thing = {
  "C": 5,
  "Frame": 0,
  "Frames": [0, 10, 1],
  "FPS": 12,
  "Flags": [1, 1, 1, 0, 1, 1, 1, 1],
  "Shapes": [
    ["Sphere", [[3.0, -2.0, 0.0], 1], [[0.0, 2.0, 0.0], [3.0, 0.0, 0.0]]]
  ]
}

shapes = []
with open("StarPositions.csv", "r") as f:
    for line in f:
        data = line.split(",")
        shapes.append([
            "Sphere",
            [(spherical_to_cartesian([float(data[1]), float(data[2])])*float(data[0])).tolist(), float(data[0])*0.2],
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        ])

print(shapes[0])
thing["Shapes"] = shapes
json.dump(thing, open("Stars.json", "w"), indent=6)
'''
data = """4.2465±0.0003
4.3441±0.0022
4.3441±0.0022
5.9629±0.0004
6.5029±0.0011
6.5029±0.0011
7.430±0.041
7.8558±0.0013
8.3044±0.0007
8.7094±0.0054
8.7094±0.0054
8.724±0.012
8.724±0.012
9.7063±0.0009
10.3057±0.0014
10.4749±0.0037
10.7241±0.0007
11.0074±0.0011
11.109±0.034
11.109±0.034
11.109±0.034
11.402±0.032
11.402±0.032
11.4039±0.0012
11.4039±0.0012
11.4908±0.0009
11.4908±0.0009
11.6191±0.0008
11.6191±0.0008
11.6797±0.0027
11.8670±0.0041
11.8670±0.0041
11.8670±0.0041
11.9118±0.0074
11.9839±0.0014
12.1222±0.0015
12.3485±0.0019
12.4970±0.0045
12.8308±0.0008
12.9472±0.0018
13.0638±0.0070
13.0638±0.0070
13.0724±0.0052
13.0724±0.0052
13.1932±0.0027
13.363±0.040
13.363±0.040
13.43±0.13
14.0500±0.0016
14.0718±0.0011
14.1747±0.0022
14.5780±0.0046
14.595±0.031
14.595±0.031
14.8395±0.0014
14.8492±0.0018
14.8706±0.0041
15.1226±0.0013
15.2001±0.0034
15.2001±0.0034
15.2001±0.0034
15.22±0.20
15.2382±0.0025
15.450±0.041
15.7586±0.0034
15.8060±0.0036
15.877±0.014
15.8857±0.0017
15.9969±0.0026
15.9969±0.0026
16.1939±0.0024
16.2005±0.0019
15.9969±0.0026
15.9969±0.0026
16.1939±0.0024
16.2005±0.0019
16.3328±0.0026
16.3330±0.0042
16.3330±0.0042
16.3330±0.0042
16.4761±0.0018
16.7074±0.0087
16.7074±0.0087
16.730±0.049
16.800±0.011
16.856±0.052
16.9861±0.0027
17.002±0.037
17.1368±0.0017
17.3738±0.0046
17.41±0.44
17.5309±0.0026
17.7263±0.0024
17.9925±0.0020
17.9925±0.0020
18.20±0.14
18.2146±0.0028
18.3305±0.0038
18.49±0.24
18.5534±0.0049
18.6042±0.0022
18.62±0.18
18.7906±0.0018
18.7993±0.0081
18.8883±0.0031
19.1987±0.0074
19.2078±0.0053
19.2724±0.0067
19.2745±0.0032
19.2922±0.0027
19.2922±0.0027
19.2996±0.0031
19.3314±0.0025
19.4185±0.0036
19.4185±0.0036
19.4185±0.0036
19.5330±0.0040
19.54±0.24
19.577±0.035
19.609±0.013
19.7045±0.0093
19.7414±0.0076
19.893±0.015
19.955±0.057
19.96±0.22
20.1062±0.0028
20.17±0.25
20.2588±0.0015
20.3947±0.0070
20.4277±0.0044
20.4277±0.0044
20.5494±0.0039
20.62±0.34
20.6575±0.0026
20.7388±0.0071
20.82±0.18
20.94±0.10
20.9615±0.0070"""

out = ""
for line in data.split("\n"):
    a = [float(x) for x in line.split("±")]
    a = a[0]
    out += str(a) + "\n"

print(out)
pyperclip.copy(out)
'''

'''
data = """14h 29m 43.0s
14h 39m 36.5s
14h 39m 35.1s
17h 57m 48.5s
10h 49m 18.9s
10h 49m 18.9s
08h 55m 10.8s
10h 56m 29.2s
11h 03m 20.2s
06h 45m 08.9s
06h 45m 08.9s
01h 39m 01.3s
01h 39m 01.3s
18h 49m 49.4s
23h 41m 54.7s
03h 32m 55.8s
23h 05m 52.0s
11h 47m 44.4s
22h 38m 33.4s
22h 38m 33.4s
22h 38m 33.4s
07h 39m 18.1s
07h 39m 18.1s
21h 06m 53.9s
21h 06m 55.3s
18h 42m 46.7s
18h 42m 46.9s
00h 18m 22.9s
00h 18m 22.9s
08h 29m 49.5s
22h 03m 21.7s
22h 04m 10.5s
22h 04m 10.5s
01h 44m 04.1s
03h 35m 59.7s
01h 12m 30.6s
07h 27m 24.5s
02h 53m 00.9s
05h 11m 40.6s
21h 17m 15.3s
18h 45m 05.3s
18h 45m 02.6s
22h 27m 59.5s
22h 27m 59.5s
10h 48m 14.7s
06h 29m 23.4s
06h 29m 23.4s
07h 22m 27.3s
16h 30m 18.1s
00h 49m 09.9s
00h 05m 24.4s
02h 00m 13.2s
12h 33m 17.2s
12h 33m 17.2s
17h 36m 25.9s
17h 28m 39.9s
10h 48m 12.6s
11h 45m 42.9s
19h 53m 54.2s
19h 53m 55.2s
19h 53m 54.2s
17h 41m 24.2s
22h 53m 16.7s
16h 39m 40.9s
10h 44m 21.2s
00h 06m 43.8s
02h 55m 03.7s
10h 11m 22.1s
11h 05m 28.6s
11h 05m 30.4s
10h 19m 36.4s
21h 33m 34.0s
11h 05m 28.6s
11h 05m 30.4s
10h 19m 36.4s
21h 33m 34.0s
17h 37m 03.7s
04h 15m 16.3s
04h 15m 21.8s
04h 15m 21.5s
22h 46m 49.7s
18h 05m 27.4s
18h 05m 27.5s
19h 50m 47.0s
08h 58m 15.2s
15h 06m 52.4s
06h 00m 03.5s
08h 17m 30.1s
11h 47m 41.4s
15h 40m 43.5s
09h 39m 35.5s
05h 01m 57.4s
13h 45m 43.8s
04h 31m 11.5s
04h 31m 12.6s
11h 14m 51.3s
06h 54m 49.0s
20h 52m 33.0s
03h 50m 00.3s
18h 35m 37.9s
05h 31m 27.4s
04h 15m 19.5s
06h 10m 34.6s
19h 32m 21.6s
05h 42m 09.3s
14h 57m 28.0s
17h 46m 32.4s
19h 20m 48.0s
23h 49m 12.5s
19h 16m 55.3s
19h 16m 57.6s
15h 32m 12.9s
00h 49m 06.3s
17h 15m 20.9s
17h 15m 21.0s
17h 16m 13.4s
07h 44m 40.2s
15h 41m 51.6s
00h 15m 28.1s
20h 11m 11.93s
03h 19m 55.7s
07h 10m 01.8s
20h 08m 43.6s
01h 36m 57s
09h 37m 34.9s
20h 13m 53.4s
22h 09m 05.7s
17h 48m 08.2s
14h 34m 16.8s
23h 31m 52.2s
23h 31m 52.6s
15h 19m 26.8s
14h 05m 18.3s
09h 14m 22.8s
09h 00m 23.6s
17h 12m 07.91s
15h 03m 19.6s
03h 39m 35.2s"""
out = ""
for line in data.split("\n"):
    a = [float(x[:-1]) for x in line.split(" ")]
    a = ((a[0]+a[1]/60+a[2]/3600)/24)*360
    out += str(a) + "\n"

print(out)
pyperclip.copy(out)
'''

'''
data = """−62° 40′ 46″
−60° 50′ 02″
−60° 50′ 14″
+04° 41′ 36″
−53° 19′ 10″
−53° 19′ 10″
−07° 14′ 43″
+07° 00′ 53″
+35° 58′ 12″
−16° 42′ 58″
−16° 42′ 58″
−17° 57′ 01″
−17° 57′ 01″
−23° 50′ 10″
+44° 10′ 30″
−09° 27′ 30″
−35° 51′ 11″
+00° 48′ 16″
−15° 17′ 57″
−15° 17′ 57″
−15° 17′ 57″
+05° 13′ 30″
+05° 13′ 30″
+38° 44′ 58″
+38° 44′ 31″
+59° 37′ 49″
+59° 37′ 37″
+44° 01′ 23″
+44° 01′ 23″
+26° 46′ 37″
−56° 47′ 10″
−56° 46′ 58″
−56° 46′ 58″
−15° 56′ 15″
−44° 30′ 45″
−16° 59′ 56″
+05° 13′ 33″
+16° 52′ 53″
−45° 01′ 06″
−38° 52′ 03″
−63° 57′ 48″
−63° 57′ 52″
+57° 41′ 45″
+57° 41′ 45″
−39° 56′ 06″
−02° 48′ 50″
−02° 48′ 50″
–05° 40′ 30″
−12° 39′ 45″
+05° 23′ 19″
−37° 21′ 27″
+13° 03′ 08″
+09° 01′ 15″
+09° 01′ 15″
+68° 20′ 21″
−46° 53′ 43″
−11° 20′ 14″
−64° 50′ 29″
+44° 24′ 55″
+44° 24′ 56″
+44° 24′ 55″
+25° 53′ 19″
−14° 15′ 49″
−68° 47′ 46″
−61° 12′ 36″
−07° 32′ 22″
−47° 00′ 52″
+49° 27′ 15″
+43° 31′ 36″
+43° 31′ 18″
+19° 52′ 10″
−49° 00′ 32″
+43° 31′ 36″
+43° 31′ 18″
+19° 52′ 10″
−49° 00′ 32″
–44° 19′ 09″
−07° 39′ 10″
−07° 39′ 29″
−07° 39′ 22″
+44° 20′ 02″
+02° 29′ 59″
+02° 29′ 56″
+08° 52′ 06″
+19° 45′ 47″
70° 27′ 25″
+02° 42′ 24″
−61° 55′ 16″
+78° 41′ 28″
−51° 01′ 36″
−24° 48′ 28″
−06° 56′ 46″
+14° 53′ 29″
+58° 58′ 37″
+58° 58′ 41″
−26° 18′ 24″
+33° 16′ 05″
−16° 58′ 29″
−56° 58′ 30″
+32° 59′ 55″
−03° 40′ 38″
−09° 35′ 07″
−21° 51′ 53″
+69° 39′ 40″
+12° 29′ 21″
−21° 24′ 56″
−57° 19′ 09″
−45° 33′ 30″
+02° 24′ 04″
+05° 10′ 08″
+05° 09′ 02″
−41° 16′ 32″
+57° 48′ 55″
−26° 36′ 09″
−26° 36′ 10″
−26° 32′ 46″
+03° 33′ 09″
−22° 50′ 25″
−16° 08′ 02″
–36° 06′ 04″
−43° 04′ 11″
38° 31′ 46″
−66° 10′ 55″
+09° 33′ 47″
29° 31′ 41″
−45° 09′ 50″
+27° 11′ 44″
+70° 52′ 35″
−12° 31′ 10″
+19° 56′ 14″
+19° 56′ 14″
−07° 43′ 20″
+55° 34′ 21″
52° 41′ 12″
+21° 50′ 05″
+45° 39′ 57″
+25° 25′ 20″
–35° 25′ 44″"""

out = ""
for line in data.split("\n"):
    sign = line[0] == "+"
    a = [int(x[:-1]) for x in line[1:].split(" ")]
    a = (abs(a[0]) + a[1]/60 + a[2]/3600) * (sign*2-1)
    out += str(a) + "\n"

print(out)
pyperclip.copy(out)
'''