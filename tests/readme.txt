from ad-sample4.txt

This doesn't parse correctly.
should find: 21 West Street, NY, NY

Notes: after the preprocessing, what's left is
'21 West Street - 21 West Street', which has no borough information.
This should be addressed when we handle parsing block codes, and perhaps
the Borough of (queens|manhatta|etc..) should skip this occurence (could
be done with regex pre and post conditional matches)

CERTIFICATE OF APPROPRIATENESS
BOROUGH OF MANHATTAN 15-6223 – Block 15, lot 22-
21 West Street - 21 West Street Building-Individual Landmark
An Art Deco style office building designed by Starrett & Van Vleck and
built in 1929-31. Application is to install a removable flood mitigation
system. Community District 1.
