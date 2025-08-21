from datetime import datetime

from hamcrest import (
    assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to,
    contains_inanyorder, has_length, none
)

from dm_api_account.models.UserDetailsEnvelope import ColorSchema
from dm_api_account.models.UserEnvelope import UserRole


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account.account_api.get_v1_account()

    assert_that(
        response,
        has_property(
            "resource",
            all_of(
                has_properties({
                    "login": starts_with("DarrenDalton12_08_2025_22_43_04"),
                    "roles": all_of(
                        contains_inanyorder(UserRole.GUEST, UserRole.PLAYER),
                        has_length(2)
                    ),
                    "online": instance_of(datetime),
                    "registration": instance_of(datetime),
                    "info": equal_to(""),
                    "medium_picture_url": none(),
                    "small_picture_url": none(),
                    "status": none(),
                    "name": none(),
                    "location": none(),
                    "icq": none(),
                    "skype": none(),
                    "original_picture_url": none(),
                    "rating": has_properties({
                        "enabled": equal_to(True),
                        "quality": equal_to(0),
                        "quantity": equal_to(0),
                    }),
                    "settings": has_properties({
                        "colorSchema": equal_to(ColorSchema.MODERN),
                        "nannyGreetingsMessage": none(),
                        "paging": has_properties({
                            "posts_per_page": equal_to(10),
                            "commentsPerPage": equal_to(10),
                            "topicsPerPage": equal_to(10),
                            "messagesPerPage": equal_to(10),
                            "entitiesPerPage": equal_to(10),
                        }),
                    }),
                })
            )
        )
    )


def test_get_v1_account(account_helper):
    response = account_helper.dm_account.account_api.get_v1_account(validate_response=False)
    assert response.status_code == 401, 'Удалось получить данные не авторизованного клиента'
