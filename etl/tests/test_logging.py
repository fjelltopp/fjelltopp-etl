import unittest
import boto3
import uuid
from etl.logging import get_logger
import time


class TestLogging(unittest.TestCase):
    def test_logging(self):
        """ Testing logging to cloudwatch"""

        log_group_name = "test-etl"
        log_name = "test-etl"
        logger = get_logger(log_name=log_name,
                            log_group=log_group_name)

        message = str(uuid.uuid4())
        logger.info(message)
        time.sleep(62)
        log_client = boto3.client('logs')

        events = log_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_name)
        self.assertEqual(events["events"][-1]["message"], message)
        
    
