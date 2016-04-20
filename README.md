# nameko-sendgrid

## Usages

#### Standalone Usage

For non-nameko services, it is still useful to be able to run RPC calls into this microservice using the nameko conventions.
The example below can be adapted for standalone services of this type.

```
from nameko.standalone.rpc import ClusterRpcProxy

config = {
    'AMQP_URI': AMQP_URI  # e.g. "amqp://guest:guest@localhost"
}

cluster_rpc = ClusterRpcProxy(config)

# To send a simple email.

cluster_rpc.sendgrid.send_email(
	to_email="Test Account <test@test.com>",
	from_email="sendertest@test.com",
	subject="test subject",
	body_html="test body html",
	body_text="test body text",
)

# To send an email with a known template, substituting variables with values given in a dictionary.

cluster_rpc.sendgrid.send_templated_email(
	to_email="Test Account <test@test.com>",
	from_email="sendertest@test.com",
	subject="test subject",
	template_id="MY-FAVORITE-TEMPLATE-ID",
	template_context={
		'some': 'first_value',
		'another': 'second_value',
	},
)

# To get a list of available templates as dictionaries of information.
# This dictionary will take the form:
#{
#	"templates": [
#		{
#			"name": "Postmaster Example", 
#			"versions": [{
#				"active": 1, 
#				"updated_at": "2016-04-19 19:33:14", 
#				"id": "ca268ce9-032f-47c5-9c46-343f62ecec51", 
#				"name": "Postmaster Example Version 1", 
#				"template_id": "143380c2-a369-45a5-999f-7d344ac24e38", 
#				"subject": "<%subject%> This is a test email using a template"
#			}], 
#			"id": "143380c2-a369-45a5-999f-7d344ac24e38"
#		}
#	]
#}


templates = cluster_rpc.sendgrid.get_available_templates()
```

## Development

#### Environment Setup

Create a virtual python environment for this project:
```
pip install virtualenv
virtualenv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
