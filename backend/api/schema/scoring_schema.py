from pydantic import (
    BaseModel,
    Field
)


class CreditInput(BaseModel):

    # =====================================================
    # FINANCIAL INFORMATION
    # =====================================================

    AMT_INCOME_TOTAL: float = Field(
        ...,
        description="Revenu annuel total du client"
    )

    AMT_CREDIT: float = Field(
        ...,
        description="Montant total du crédit demandé"
    )

    AMT_ANNUITY: float = Field(
        ...,
        description="Montant des mensualités du prêt"
    )

    AMT_GOODS_PRICE: float = Field(
        ...,
        description="Prix du bien financé"
    )

    # =====================================================
    # CLIENT INFORMATION
    # =====================================================

    DAYS_BIRTH: int = Field(
        ...,
        description="Âge du client en jours négatifs"
    )

    DAYS_EMPLOYED: int = Field(
        ...,
        description="Ancienneté emploi en jours négatifs"
    )

    CNT_CHILDREN: int = Field(
        ...,
        description="Nombre d'enfants"
    )

    CODE_GENDER: str = Field(
        ...,
        description="Genre du client (M/F)"
    )

    # =====================================================
    # EDUCATION & INCOME
    # =====================================================

    NAME_EDUCATION_TYPE: str = Field(
        ...,
        description="Niveau d'éducation du client"
    )

    NAME_INCOME_TYPE: str = Field(
        ...,
        description="Type de revenu du client"
    )

    # =====================================================
    # REGION
    # =====================================================

    REGION_RATING_CLIENT_W_CITY: int = Field(
        ...,
        description="Score de la région du client"
    )

    # =====================================================
    # EXTERNAL SCORES
    # =====================================================

    EXT_SOURCE_1: float = Field(
        ...,
        description="Score externe 1"
    )

    EXT_SOURCE_2: float = Field(
        ...,
        description="Score externe 2"
    )

    EXT_SOURCE_3: float = Field(
        ...,
        description="Score externe 3"
    )