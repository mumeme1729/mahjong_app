


def get_uma(rank_id:int, rank):
    uma = {
        "10": {"1":25, "2":10, "3":0,"4":-15},
        "20": {"1":35, "2":15, "3":0,"4":-25},
        "21": {"1":35, "2":15, "3":-5,"4":-35},
        "22": {"1":35, "2":15, "3":-5,"4":-45},
        "30": {"1":55, "2":25, "3":-5,"4":-105},
        "40": {"1":70, "2":35, "3":-5,"4":-145},
        "50": {"1":100, "2":50, "3":-50,"4":-250},
    } 

    score = uma.get(str(rank_id))
    return score.get(str(rank))

