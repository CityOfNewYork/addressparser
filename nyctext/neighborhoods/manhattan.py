from regexps import make_neighorbood_regex

_hoods = '''Alphabet City
Astor Row
Battery Park City
Bowery
Carnegie Hill
Chelsea
Chinatown
Civic Center
Columbus Circle
Cooperative Village
Diamond District
East Harlem
East Village
Ellis Island
Essex Crossing
Financial District
Five Points
Flatiron District
Garment District
Gashouse District
Governors Island
Gramercy Park
Greenwich Village
Hamilton Heights
Harlem
Hells Kitchen
Herald Square
Hudson Heights
Hudson Square
Hudson Yards
Inwood
Kips Bay
Koreatown
Lenox Hill
Le Petit Senegal
Liberty Island
Lincoln Square
Little Fuzhou
Little Germany
Little Italy
Little Spain
Little Syria
Lower East Side
Lower Manhattan
Madison Square
Manhattan Valley
Manhattantown
Manhattanville
Marble Hill
Marcus Garvey Park
Meatpacking District
Midtown Manhattan
Morningside Heights
Murray Hill
NoHo
Nolita
NoMad
Penn South
Peter Cooper Village
Pomander Walk
Radio Row
Randalls Island
Riverside South
Roosevelt Island
Rose Hill
Silicon Alley
SoHo
South Street Seaport
South Village
Stuyvesant Square
Stuyvesant Town
Sugar Hill
Sutton Place
Sylvan
Tenderloin
Theater District
Times Square
Tribeca
Tudor City
Turtle Bay
Two Bridges
Union Square
Upper East Side
Upper Manhattan
Upper West Side
Wards Island
Washington Heights
Waterside Plaza
West Village
World Trade Center
Yorkville'''.split('\n')

r_manhattan = make_neighorbood_regex(_hoods, 'manhattan|ny')
