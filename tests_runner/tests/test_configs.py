from tests_runner.utils.configs import Configuration
import pytest
import os

def setup_base_config():
    Configuration._instance = None
    os.environ['STRAPI_TOKEN'] = 'test'

def test_no_strapi_token():
    Configuration._instance = None

    with pytest.raises(ValueError):
        config = Configuration()

def test_config_singleton():
    setup_base_config()

    first = Configuration()
    second = Configuration()

    assert first is second


def test_config_change_value():
    setup_base_config()

    config = Configuration()

    with pytest.raises(AttributeError):
        config.REDIS_HOST = "test"

    with pytest.raises(AttributeError):
        config.REDIS_PORT = "test"

    with pytest.raises(AttributeError):
        config.REDIS_QUEUE_NAME = "test"

    with pytest.raises(AttributeError):
        config.STRAPI_BASE_URL = "test"

    with pytest.raises(AttributeError):
        config.STRAPI_TOKEN = "test"



def test_config_default_values():
    setup_base_config()

    config = Configuration()

    assert config.REDIS_HOST == '127.0.0.1'
    assert config.REDIS_PORT == '6379'
    assert config.REDIS_QUEUE_NAME == 'security_tests'
    assert config.STRAPI_BASE_URL == 'http://127.0.0.1:1337'
    assert config.STRAPI_TOKEN == 'test'


def test_config_custom_values():
    custom_redis_host = "custom_host"
    custom_redis_port = "12345"
    custom_redis_queue_name = "custom_queue"
    custom_strapi_base_url = "http://custom-url:1337"
    custom_strapi_token = "custom_token"

    os.environ['REDIS_HOST'] = custom_redis_host
    os.environ['REDIS_PORT'] = custom_redis_port
    os.environ['REDIS_QUEUE_NAME'] = custom_redis_queue_name
    os.environ['STRAPI_BASE_URL'] = custom_strapi_base_url
    os.environ['STRAPI_TOKEN'] = custom_strapi_token

    Configuration._instance = None

    config = Configuration()

    assert config.REDIS_HOST == custom_redis_host
    assert config.REDIS_PORT == custom_redis_port
    assert config.REDIS_QUEUE_NAME == custom_redis_queue_name
    assert config.STRAPI_BASE_URL == custom_strapi_base_url
    assert config.STRAPI_TOKEN == custom_strapi_token
