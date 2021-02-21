from django.apps import AppConfig

from nuvox_algorithm import NuvoxAlgorithm


class KeyboardConfig(AppConfig):
    name = 'keyboard'

    nuvox_algorithm = NuvoxAlgorithm()
