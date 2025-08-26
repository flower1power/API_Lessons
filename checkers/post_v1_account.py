from datetime import datetime

import allure
from hamcrest import assert_that, all_of, starts_with, has_property, instance_of, has_properties, equal_to


class PostV1Account:

    @classmethod
    @allure.step("Проверка ответа POST v1/account")
    def check_response_values(cls, prepare_user, response):
        today = datetime.now().strftime('%Y-%m-%d')

        assert_that(str(response.resource.registration), starts_with(today))

        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with(prepare_user.login))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
                    'resource', has_properties(
                        'rating', has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    )
                ),
            )
        )
