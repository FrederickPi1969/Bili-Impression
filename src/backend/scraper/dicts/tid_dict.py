
"""
How would you specify the subarea for this query?
[0] All Subarea (choose this if you have no clue)
[1] Animation
[2] Bangumi
[3] Domestic
[4] Music
[5] Dance 
[6] Game
[7] Knowledge
[8] Digital Tech
[9] Lifestyle
[10] Food
[11] Autotune Remix
[12] Fashion
[13] News
[14] Entertainment
[15] Television
[16] Documentary 
[17] Film and Movie
[18] TV Series

Above are the selectable subareas to be used
for filtering video results.
For each of the given index (0-18),
the dicts below direct it to
its corresponding tid to be inserted into urls.
"""

idx2tid = {
    "0" : "0",
    "1" : "1",
    "2" : "13",
    "3" : "167",
    "4" : "3",
    "5" : "129",
    "6" : "4",
    "7" : "36",
    "8" : "188",
    "9" : "160",
    "10" : "211",
    "11" : "119",
    "12" : "155",
    "13" : "202",
    "14" : "5",
    "15" : "181",
    "16" : "177",
    "17" : "23",
    "18" : "11"
}

tid2idx = {v : k for k, v in idx2tid.items()}