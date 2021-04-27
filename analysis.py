class Analysis:
    def __init__(self) -> None:
        self.title = ""
        self.period = None
        self.hotspots = None
        self.hs_bv = ""
        self.observations = {}
        self.target_species = None
        self.seen_species = None

    @classmethod
    def new_analysis(cls, loc_ids: list, period: int) -> "Analysis":
        """Return a new Analysis object for the supplied hostpots and period."""
        pass

    def trip_from_bv(self, bv: str) -> "Trip":
        pass

    @staticmethod
    def _bv_to_bools(bv: str) -> list:
        out_bools = []
        for c in bv:
            out_bools.append(c == "1")
        return out_bools


class Trip:
    def __init__(self) -> None:
        self.title = ""
        self.period = None
        self.hs_bv = None
        self.hotspots = None
        self.observations = {}
        self.specialties = {}
