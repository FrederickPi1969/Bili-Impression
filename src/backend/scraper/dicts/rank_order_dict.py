"""
Option ID to rank order of video results.
Notice the order names are intended to be 
directly inserted to urls.
"""
idx2rank_order = {
    "0" : "totalrank", 
    "1" : "click",
    "2" : "pubdate",
    "3" : "dm",
    "4" : "stow"
}

rank_order2idx = {v : k for k, v in idx2rank_order.items()}