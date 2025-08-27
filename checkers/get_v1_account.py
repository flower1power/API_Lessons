from datetime import datetime

import allure
from hamcrest import (
    assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to,
    contains_inanyorder, has_length, none
)

from dm_api_account.models.UserDetailsEnvelope import ColorSchema
from dm_api_account.models.UserEnvelope import UserRole


class GetV1Account:
    @classmethod
    @allure.step("Проверка ответа метода GET v1_account")
    def check_response_values(cls, response, login):
        assert_that(
            response,
            has_property(
                "resource",
                all_of(
                    has_properties({
                        "login": starts_with(login),
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
