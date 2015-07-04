from regexps import make_neighorbood_regex

_hoods = '''Arverne
Astoria
Astoria Heights
Auburndale
Bay Terrace
Bayside
Bayswater
Beechhurst
Bellaire
Belle Harbor
Bellerose
Blissville
Breezy Point
Briarwood
Broad Channel
Broadway-Flushing
Brookville
Cambria Heights
Chinatown
College Point
Corona
Ditmars
Douglaston
Downtown Flushing
Dutch Kills
East Elmhurst
Edgemere
Electchester
Elmhurst
Far Rockaway
Floral Park
Flushing
Forest Hills
Forest Hills Gardens
Fort Totten
Fresh Meadows
Fresh Pond
Glen Oaks
Glendale
Hamilton Beach
Hammels
Hillcrest
Hollis
Hollis Hills
Holliswood
Howard Beach
Howard Park
Hunters Point
Jackson Heights
Jamaica
Jamaica Center
Jamaica Estates
Jamaica Hills
Kew Gardens
Kew Gardens Hills
Koreatown
Laurelton
Linden Hill
Little Egypt
Little Neck
Long Island City
Malba
Maspeth
Meadowmere
Middle Village
Murray Hill
Neponsit
North Corona
Oakland Gardens
Old Howard Beach
Ozone Park
Pomonok
Queens Village
Queensboro Hill
Ramblersville
Rego Park
Richmond Hill
Ridgewood
Rockaway Beach
Rockaway Park
Rockwood Park
Rosedale
Roxbury
Saint Albans
Seaside
South Jamaica
South Ozone Park
Springfield Gardens
Sunnyside
Sunnyside Gardens
The Hole
Tudor Village
Utopia
Warnerville
Whitestone
Willets Point
Woodhaven
Woodside
Wyckoff Heights'''.split('\n')

r_queens = make_neighorbood_regex(_hoods, 'queens')
