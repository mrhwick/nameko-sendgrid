import pytest
from unittest.mock import MagicMock, patch
from src.main import SendgridService


def test_send_email_creates_message_with_correct_data():
	service = SendgridService()
	sendgrid_mock = MagicMock()
	send_method_mock = MagicMock()
	send_method_mock.return_value = (200, 'some message')
	sendgrid_mock.send = send_method_mock
	service.sendgrid_v2_client = sendgrid_mock

	with patch('src.main.sendgrid.Mail') as mail_mock:
		service.send_email(
			to_email="Test Account <test@test.com>",
			from_email="sendertest@test.com",
			subject="test subject",
			body_html="test body html",
			body_text="test body text",
		)

		mail_mock.assert_called_once_with(
			to="Test Account <test@test.com>",
			subject="test subject",
			html="test body html",
			text="test body text",
			from_email="sendertest@test.com",
		)


def test_send_email_calls_sendgrid_v2_with_created_message():
	service = SendgridService()
	
	sendgrid_mock = MagicMock()
	send_method_mock = MagicMock()
	send_method_mock.return_value = (200, 'some message')
	sendgrid_mock.send = send_method_mock
	service.sendgrid_v2_client = sendgrid_mock


	with patch('src.main.sendgrid.Mail') as mail_mock:
		return_mock = MagicMock()
		mail_mock.return_value = return_mock

		service.send_email(
			to_email="Test Account <test@test.com>",
			from_email="sendertest@test.com",
			subject="test subject",
			body_html="test body html",
			body_text="test body text",
		)

		send_method_mock.assert_called_once_with(return_mock)

def test_send_templated_email_created_message_with_correct_data():
	service = SendgridService()
	sendgrid_mock = MagicMock()
	send_method_mock = MagicMock()
	send_method_mock.return_value = (200, 'some message')
	sendgrid_mock.send = send_method_mock
	service.sendgrid_v2_client = sendgrid_mock

	with patch('src.main.sendgrid.Mail') as mail_mock:
		return_mock = MagicMock()
		mail_mock.return_value = return_mock
		service.send_templated_email(
			to_email="Test Account <test@test.com>",
			from_email="sendertest@test.com",
			subject="test subject",
			template_id="MY-FAVORITE-TEMPLATE",
			template_context={
				'some': 'first_value',
				'another': 'second_value',
			},
		)

		mail_mock.assert_called_once_with(
			to="Test Account <test@test.com>",
			from_email="sendertest@test.com",
			subject="test subject",
			html=" ",
		)
		return_mock.add_filter.assert_any_call(
			'templates',
			'enable',
			'1'
		)
		return_mock.add_filter.assert_any_call(
			'templates',
			'template_id',
			'MY-FAVORITE-TEMPLATE'
		)
		return_mock.add_substitution.assert_any_call(
			'some',
			'first_value',
		)
		return_mock.add_substitution.assert_any_call(
			'another',
			'second_value',
		)

def test_send_templated_email_without_template_context_creates_message():
	service = SendgridService()
	sendgrid_mock = MagicMock()
	send_method_mock = MagicMock()
	send_method_mock.return_value = (200, 'some message')
	sendgrid_mock.send = send_method_mock
	service.sendgrid_v2_client = sendgrid_mock

	with patch('src.main.sendgrid.Mail') as mail_mock:
		return_mock = MagicMock()
		mail_mock.return_value = return_mock
		service.send_templated_email(
			to_email="Test Account <test@test.com>",
			from_email="sendertest@test.com",
			subject="test subject",
			template_id="MY-FAVORITE-TEMPLATE",
		)

		mail_mock.assert_called_once_with(
			to="Test Account <test@test.com>",
			from_email="sendertest@test.com",
			subject="test subject",
			html=" ",
		)
		return_mock.add_filter.assert_any_call(
			'templates',
			'enable',
			'1'
		)
		return_mock.add_filter.assert_any_call(
			'templates',
			'template_id',
			'MY-FAVORITE-TEMPLATE'
		)


def test_send_templated_email_without_template_context_creates_message():
	service = SendgridService()
	sendgrid_mock = MagicMock()
	send_method_mock = MagicMock()
	send_method_mock.return_value = (200, 'some message')
	sendgrid_mock.send = send_method_mock
	service.sendgrid_v2_client = sendgrid_mock

	with patch('src.main.sendgrid.Mail') as mail_mock:
		return_mock = MagicMock()
		mail_mock.return_value = return_mock
		with pytest.raises(ValueError):
			service.send_templated_email(
				to_email="Test Account <test@test.com>",
				from_email="sendertest@test.com",
				subject="test subject",
				template_id="MY-FAVORITE-TEMPLATE",
				template_context="I don't know what I'm doing."
			)

def test_get_available_templates():
	service = SendgridService()

	expected_return_value = bytes("""{
		"templates": [
			{
				"name": "Postmaster Example", 
				"versions": [{
					"active": 1, 
					"updated_at": "2016-04-19 19:33:14", 
					"id": "ca268ce9-032f-47c5-9c46-343f62ecec51", 
					"name": "Postmaster Example Version 1", 
					"template_id": "143380c2-a369-45a5-999f-7d344ac24e38", 
					"subject": "<%subject%> This is a test email using a template"
				}], 
				"id": "143380c2-a369-45a5-999f-7d344ac24e38"
			}
		]
	}""".strip('\n\t'), encoding='UTF-8')

	response = MagicMock()
	response.response_body = expected_return_value

	service.sendgrid_v3_client = MagicMock()
	service.sendgrid_v3_client.client.templates.get = MagicMock(return_value=response)
	response = service.get_available_templates()
	assert(type(response) is dict)
	assert('templates' in response.keys())
	assert(len(response['templates']) == 1)
	assert(response['templates'][0]['name'] == "Postmaster Example")





















