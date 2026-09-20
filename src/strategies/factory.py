from src.strategies.base import IExtractionStrategy
from src.strategies.anchor_strategy import AnchorExtractionStrategy
from src.strategies.bounding_box_strategy import BoundingBoxExtractionStrategy
from src.strategies.table_strategy import TableExtractionStrategy
from src.domain.models import ExtractionRule, AnchorExtractionRule, BoundingBoxExtractionRule, TableExtractionRule

class ExtractionStrategyFactory:
    @staticmethod
    def create(rule: ExtractionRule) -> IExtractionStrategy:
        if isinstance(rule, AnchorExtractionRule):
            return AnchorExtractionStrategy(rule)
        elif isinstance(rule, BoundingBoxExtractionRule):
            return BoundingBoxExtractionStrategy(rule)
        elif isinstance(rule, TableExtractionRule):
            return TableExtractionStrategy(rule)
        else:
            raise ValueError(f"Unknown rule type: {type(rule)}")
