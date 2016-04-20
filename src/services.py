from nameko.rpc import rpc
from nameko.events import EventDispatcher, event_handler
import sendgrid
import os
from datetime import datetime
import json

class SendgridService(object):
	name = 'sendgrid'

	def __init__(self):
		self.sendgrid_key = os.environ.get('SENDGRID_API_KEY')
		self.sendgrid_v2_client = sendgrid.SendGridClient(self.sendgrid_key)
		self.sendgrid_v3_client = sendgrid.SendGridAPIClient(apikey=self.sendgrid_key)

	@rpc
	def send_email(self, to_email, from_email, subject, body_html, body_text):
		message = sendgrid.Mail(to=to_email, subject=subject, html=body_html, text=body_text, from_email=from_email)
		print("SENDGRID: send_email: Attempting to send email to {to_email} from {from_email} with subject {subject} at time {time}".format(
			to_email=to_email,
			from_email=from_email,
			subject=subject,
			time=datetime.now(),
		))
		
		status, msg = self.sendgrid_v2_client.send(message)
		
		print("SENDGRID: send_email: Received response from Sendgrid at time {time} with status {status} and response {msg}".format(
			time=datetime.now(),
			status=status,
			msg=msg,
		))

	@rpc 
	def send_templated_email(self, to_email, from_email, subject, template_id, template_context=None):
		if template_context and not isinstance(template_context, dict):
			raise ValueError("Template Context should be a dictionary of template substitutions.")

		message = sendgrid.Mail(to=to_email, from_email=from_email, subject=subject, html=" ")
		message.add_filter('templates', 'enable', '1')
		message.add_filter('templates', 'template_id', template_id)

		# Add template key/value pairs
		if template_context:
			for arg in template_context.keys():
				message.add_substitution(arg, template_context.get(arg))
		
		print("SENDGRID: send_templated_email: Attempting to send email to {to_email} from {from_email} with subject {subject} using template {template_id} at time {time}".format(
			to_email=to_email,
			from_email=from_email,
			subject=subject,
			template_id=template_id,
			time=datetime.now(),
		))
		
		status, msg = self.sendgrid_v2_client.send(message)
		
		print("SENDGRID: send_templated_email: Received response from Sendgrid at time {time} with status {status} and response {msg}".format(
			time=datetime.now(),
			status=status,
			msg=msg,
		))
		

	@rpc
	def get_available_templates(self):
		response = self.sendgrid_v3_client.client.templates.get()
		return json.loads(str(response.response_body, encoding='UTF-8'))
