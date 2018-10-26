import unittest
from etl import sources
from unittest.mock import patch, MagicMock


class TestODKSource(unittest.TestCase):
    def test_fix_odk_sunmission(self):
        """ Testing fix odk submission"""
        data = {
            "@a": "a",
            "b": "b",
            "orx:meta": "should_not_be_there"
        }

        fixed_data = sources.fix_odk_data(data)

        self.assertEqual(fixed_data, {
            "a": "a",
            "b": "b"
        })

    @patch("etl.sources.requests")
    def test_get_odk_submission(self, mock_requsts):
        """ Testing get submission"""
        result_mock = MagicMock()
        result_mock.text = '<submission xmlns="http://opendatakit.org/submissions" xmlns:orx="http://openrosa.org/xforms" ><data><test_form id="test" instanceID="uuid:7ba84cc0-ef88-4e68-95cd-256a0f4ac0f7" submissionDate="2018-10-25T13:08:58.093Z" isComplete="true" markedAsCompleteDate="2018-10-25T13:08:58.093Z"><person_name>09179615-72fd-4ec9-92d7-fa702358ea54</person_name><orx:meta><orx:instanceID>uuid:7ba84cc0-ef88-4e68-95cd-256a0f4ac0f7</orx:instanceID></orx:meta></test_form></data></submission>'
        result_mock.status_code = 200
        mock_requsts.get = MagicMock(return_value=result_mock)

        url = "http://test.test"
        auth = "http-auth"
        result = sources.get_odk_submission(url, auth, "test_form", "uuid-a")
        self.assertEqual(result["person_name"], "09179615-72fd-4ec9-92d7-fa702358ea54")

    @patch("etl.sources.requests")
    @patch("etl.sources.get_odk_submission")
    def test_get_odk_data(self,  mock_get_odk_submission,mock_requsts,):
        """ Testing get submission"""
        result_mock = MagicMock()
        result_mock.text = '<idChunk xmlns="http://opendatakit.org/submissions"><idList><id>uuid:7ba84cc0-ef88-4e68-95cd-256a0f4ac0f7</id><id>uuid:bb6e48f4-ef3c-4291-b943-42c8d2a044c1</id><id>uuid:5c1bc811-6542-4221-b50a-054db7ab13ae</id><id>uuid:5c9e3d0a-bacc-4814-b2b3-3c33b6813712</id><id>uuid:8c005761-ae11-4975-a923-e5e55cb12882</id><id>uuid:0d0047e9-8fa4-499b-a5d9-665cd072e9b5</id><id>uuid:0969f963-ae52-404f-82c5-2db451a5e1af</id><id>uuid:121c2dcb-fffd-4f83-a483-5e1ee8b29686</id><id>uuid:60c67f01-b5fa-4595-b15d-cad1f89a8e04</id></idList><resumptionCursor>&lt;cursor xmlns="http://www.opendatakit.org/cursor"&gt;&lt;attributeName&gt;_LAST_UPDATE_DATE&lt;/attributeName&gt;&lt;attributeValue&gt;2018-10-25T13:09:02.355+0000&lt;/attributeValue&gt;&lt;uriLastReturnedValue&gt;uuid:60c67f01-b5fa-4595-b15d-cad1f89a8e04&lt;/uriLastReturnedValue&gt;&lt;isForwardCursor&gt;true&lt;/isForwardCursor&gt;&lt;/cursor&gt;</resumptionCursor></idChunk>'

        result_mock.status_code = 200
        mock_requsts.get = MagicMock(return_value=result_mock)
        mock_get_odk_submission.return_value = {"a": "a"}

        data = sources.get_odk_data("test_url", "test_user",
                                    "test_password", "test_form")

        mock_get_odk_submission.assert_called_with(
            "test_url", mock_requsts.auth.HTTPDigestAuth("test_user", "test_password"),
            "test_form", "uuid:60c67f01-b5fa-4595-b15d-cad1f89a8e04")

        self.assertEqual(data.columns, ["a"])
        self.assertEqual(len(data), 9)
