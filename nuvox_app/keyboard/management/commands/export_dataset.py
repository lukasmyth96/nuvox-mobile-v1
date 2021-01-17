from typing import List

from django.core.management import BaseCommand

from definition import TRACE_ALGORITHM_DATASET_TRAIN_PATH, TRACE_ALGORITHM_DATASET_TEST_PATH
from nuvox_algorithm.utils.io_funcs import write_json_file
from keyboard.models import DataCollectionSwipe, DatasetSplit


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Exports dataset of swipes to train.json and test.json files.

        Notes
        - 'target_text' label is set to None for test set
        - swipes where 'trace_matches_text' is False are not included.
        """
        train_swipes = DataCollectionSwipe.objects.filter(dataset_split=DatasetSplit.TRAIN, trace_matches_text=True)
        self.save_split(swipes=train_swipes, include_labels=True, output_path=TRACE_ALGORITHM_DATASET_TRAIN_PATH)

        test_swipes = DataCollectionSwipe.objects.filter(dataset_split=DatasetSplit.TEST, trace_matches_text=True)
        self.save_split(swipes=test_swipes, include_labels=False, output_path=TRACE_ALGORITHM_DATASET_TEST_PATH)

    @staticmethod
    def save_split(swipes: List[DataCollectionSwipe],
                   include_labels: bool,
                   output_path: str):
        json_data = []
        for swipe in swipes:
            json_data.append(
                {
                    'id': swipe.id,
                    'user_id': swipe.user.id,
                    'device_type': swipe.device_type,
                    'trace': swipe.trace,
                    'target_text': swipe.target_text if include_labels else None,
                }
            )

        write_json_file(file_path=output_path, data=json_data)
