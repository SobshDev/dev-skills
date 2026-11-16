# accounts service

Postgres 16. Migrations in migrations/ are applied in order by our deploy pipeline
before the new app version starts rolling out. The app runs as 3 instances behind a
load balancer and is deployed with rolling updates (one instance at a time).
