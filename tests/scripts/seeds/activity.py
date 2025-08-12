from src.schemas.activity import ActivityIn


def get_activity_seeds() -> list[ActivityIn]:
    return [
        ActivityIn(name="IT"),
        ActivityIn(
            name="Продукты",
            children=[
                ActivityIn(
                    name="Животноводство",
                    children=[
                        ActivityIn(name="Мясная продукция"),
                        ActivityIn(name="Молочная продукция"),
                    ],
                ),
                ActivityIn(
                    name="Растениеводство", children=[ActivityIn(name="Огороды")]
                ),
            ],
        ),
        ActivityIn(
            name="Финансы",
            children=[
                ActivityIn(name="Банки"),
                ActivityIn(
                    name="Кредитные организации",
                    children=[
                        ActivityIn(name="Микрокредиты"),
                        ActivityIn(name="Микрозаймы"),
                    ],
                ),
            ],
        ),
        ActivityIn(
            name="Бюджетные организации",
            children=[
                ActivityIn(
                    name="Муниципальные",
                    children=[
                        ActivityIn(name="Школы"),
                        ActivityIn(name="Детские сады"),
                    ],
                ),
                ActivityIn(
                    name="Федеральные", children=[ActivityIn(name="Министерства")]
                ),
            ],
        ),
    ]
