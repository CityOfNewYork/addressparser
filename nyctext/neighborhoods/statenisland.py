from regexps import make_neighorbood_regex

_hoods = '''Annadale
Arden Heights
Arlington
Arrochar
Bay Terrace
Bloomfield
Brighton Heights
Bulls Head
Castleton
Castleton Corners
Charleston
Chelsea
Clifton
Concord
Dongan Hills
Egbertville
Elm Park
Eltingville
Emerson Hill
Fort Wadsworth
Graniteville
Grant City
Grasmere
Great Kills
Greenridge
Grymes Hill
Hamilton Park
Heartland Village
Huguenot
Lighthouse Hill
Livingston
Manor Heights
Mariners Harbor
Meiers Corners
Midland Beach
New Brighton
New Dorp
New Springville
Oakwood
Ocean Breeze
Old Place
Old Town
Pleasant Plains
Port Richmond
Prince's Bay
Randall Manor
Richmond Valley
Richmondtown
Rosebank
Rossville
Sandy Ground
Shore Acres
Silver Lake
South Beach
St. George
Stapleton
Stapleton Heights
Sunnyside
Todt Hill
Tompkinsville
Tottenville
Tottenville Beach
Travis
Ward Hill
Westerleigh
West New Brighton
Willowbrook
Woodrow'''.split('\n')

r_statenIsland = make_neighorbood_regex(_hoods, 'staten island')
