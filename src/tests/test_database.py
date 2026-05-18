import unittest
from unittest.mock import patch

from src.backend import database


class InitDatabaseTests(unittest.TestCase):
    def test_manga_maniacs_seed_data_matches_issue_details(self):
        self.assertEqual(
            database.initial_activities["Manga Maniacs"],
            {
                "description": "Explore the fantastic stories of the most interesting characters from Japanese Manga (graphic novels).",
                "schedule": "Tuesdays, 7:00 PM - 8:00 PM",
                "schedule_details": {
                    "days": ["Tuesday"],
                    "start_time": "19:00",
                    "end_time": "20:00",
                },
                "max_participants": 15,
                "participants": [],
            },
        )

    @patch.object(database, "teachers_collection")
    @patch.object(database, "activities_collection")
    def test_init_database_upserts_missing_seed_activities(
        self, mock_activities_collection, mock_teachers_collection
    ):
        mock_teachers_collection.count_documents.return_value = 1

        database.init_database()

        mock_activities_collection.update_one.assert_any_call(
            {"_id": "Manga Maniacs"},
            {"$setOnInsert": database.initial_activities["Manga Maniacs"]},
            upsert=True,
        )
        self.assertEqual(
            mock_activities_collection.update_one.call_count,
            len(database.initial_activities),
        )


if __name__ == "__main__":
    unittest.main()
