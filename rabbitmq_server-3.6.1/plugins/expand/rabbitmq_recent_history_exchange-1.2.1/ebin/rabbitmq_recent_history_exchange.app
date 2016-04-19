{application, rabbitmq_recent_history_exchange,
 [{description, "RabbitMQ Recent History Exchange"},
  {vsn, "1.2.1"},
  {modules, ['rabbit_exchange_type_recent_history']},
  {registered, []},
  {applications, [kernel, stdlib, rabbit, mnesia]}]}.
