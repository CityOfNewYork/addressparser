import re

_neighborhoods = '''Bedford Park
Belmont
Fordham
Kingsbridge
Kingsbridge Heights
Van Cortlandt Village
Marble Hill
Norwood
Riverdale
Central Riverdale
Fieldston
North Riverdale
Spuyten Duyvil
South Riverdale
University Heights
Woodlawn
Downtown Bronx
Concourse Village
East Tremont
Highbridge
Hunts Point
Longwood
Foxhurst
Woodstock
Melrose
Morris Heights
Morrisania
Crotona Park East
Mott Haven
Port Morris
The Hub
Tremont
Mount Eden
Mount Hope
West Farms
Allerton
Baychester
Bronxdale
City Island
Co-op City
Eastchester
Edenwald
Indian Village
Laconia
Olinville
Morris Park
Pelham Gardens
Pelham Parkway
Van Nest
Wakefield
Williamsbridge
Bronx River
Bruckner
Castle Hill
Clason Point
Country Club
Edgewater Park
Harding Park
Parkchester
Park Versailles
Westchester Heights
Pelham Bay
Pelham Bay Park
Orchard Beach
Soundview
Schuylerville
Throg{1,2}s Neck
Unionport
Westchester Square'''.split('\n')

_hoods = [r'%s[\s,]' % n for n in _neighborhoods]
_hoods = '|'.join(_hoods)
_hoods = '(%s)(?!\s+(Avenue|Street|Parkway))' % _hoods
rex_neighborhoods_bronx = re.compile(_hoods, re.I)
