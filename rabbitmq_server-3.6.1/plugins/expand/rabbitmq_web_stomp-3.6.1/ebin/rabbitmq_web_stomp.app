{application, rabbitmq_web_stomp,
 [
  {description, "Rabbit WEB-STOMP - WebSockets to Stomp adapter"},
  {vsn, "3.6.1"},
  {modules, ['rabbit_ws_app','rabbit_ws_client','rabbit_ws_client_sup','rabbit_ws_handler','rabbit_ws_sockjs','rabbit_ws_sup']},
  {registered, []},
  {mod, {rabbit_ws_app, []}},
  {env, [{port, 15674},
         {tcp_config, []},
         {num_tcp_acceptors, 10},
         {ssl_config, []},
         {num_ssl_acceptors, 1},
         {cowboy_opts, []},
         {sockjs_opts, []},
         {ws_frame, text}]},
  {applications, [kernel, stdlib, rabbit, rabbitmq_stomp, cowboy, sockjs]}
 ]}.
