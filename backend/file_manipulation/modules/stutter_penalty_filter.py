from ..core.base_filter import QualityFilter
from ..datatypes.text_candidate import TextCandidate
from ..utils.text_analyzer import TextAnalyzer


class StutterPenaltyFilter(QualityFilter):
    """
    Filtro que penaliza repetições excessivas de caracteres (gagueira).
    """

    def filter(self, candidate: TextCandidate) -> float:
        analyzer = TextAnalyzer()
        metrics = analyzer.analyze_structure(candidate.text_content)
        return -1.0 if metrics.get("has_stutter", False) else 0.0
