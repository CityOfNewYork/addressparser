from regexps import make_neighorbood_regex

_hoods = '''Brooklyn Heights
Brooklyn Navy Yard
Cadman Plaza
Clinton Hill
Downtown Brooklyn
Bridge Plaza
RAMBO
DUMBO
Fort Greene
Fulton Ferry
Prospect Heights
Vinegar Hill
South Brooklyn
Boerum Hill
Carroll Gardens
Columbia Street Waterfront District
Cobble Hill
Gowanus
Park Slope
South Park Slope
Greenwood Heights
Red Hook
Bedford.Stuyvesant
Bedford
Ocean Hill
Stuyvesant Heights
Bushwick
Wyckoff Heights
East Williamsburg
Greenpoint
Little Poland
Williamsburg
Crown Heights
Weeksville
Ditmas Park
Flatbush
East Flatbush
Farragut
Fiske Terrace
Pigtown
Prospect Park area
Kensington
Ocean Parkway
Prospect Lefferts Gardens
Prospect Park South
Windsor Terrace
Wingate
Bath Beach
Bay Ridge
Bensonhurst
Borough Park
Dyker Heights
Mapleton
New Utrecht
Sunset Park
Chinatown
Sunset Industrial Park
Barren Island
Bergen Beach
Georgetown
Coney Island
Brighton Beach
Manhattan Beach
Sheepshead Bay
Madison
Sea Gate
Flatlands
Gerritsen Beach
Gravesend
White Sands
Homecrest
Marine Park
Midwood
Mill Basin
Plumb Beach
Brownsville
Canarsie
East New York
City Line
Cypress Hills
New Lots
Starrett City
Highland Park'''.split('\n')

r_brooklyn = make_neighorbood_regex(_hoods, 'brooklyn')
