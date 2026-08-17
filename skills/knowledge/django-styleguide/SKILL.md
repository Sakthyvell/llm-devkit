---
name: django-styleguide
description: Apply HackSoft's Django Styleguide as task-scoped engineering guidance. Use when the user explicitly invokes this knowledge skill, says `with django-styleguide`, or asks for Django/DRF service layers, selectors, model validation, API structure, error handling, testing, Celery task structure, or pragmatic Django project organization.
---

Use this as an active engineering standard for the current task only.

- Apply these rules alongside local project conventions and user instructions.
- Prefer concrete, scoped improvements over broad rewrites.
- If combined with other knowledge standards, reconcile conflicts in favor of the most task-specific rule.
- Do not quote or summarize the source as notes; use it to shape planning, implementation, and review decisions.

Imported from HackSoft's `Django-Styleguide`, MIT licensed.

# OBEY Django Styleguide by HackSoft

## When to use

Use when building, changing, reviewing, or refactoring Django and Django REST Framework code where business logic, data access, validation, API boundaries, errors, tests, or Celery tasks need a pragmatic structure.

## Primary bias to correct

Do not let Django convenience abstractions hide the application behavior. Keep the domain flow traceable by separating writing workflows, read queries, interface code, validation, and transport concerns.

## Decision rules

- Put business logic primarily in services, selectors, model properties for simple derived values, and model `clean` for simple object-level validation.
- Keep business logic out of APIs, views, serializers, forms, template tags, model `save`, broad custom managers, broad querysets, and signals.
- Use services for write-side operations and workflows. Prefer explicit functions in `services.py`, keyword-only arguments for multiple inputs, type annotations, `full_clean()` before `save()`, and transactions around multi-step changes.
- Use class-based services only when they provide a useful namespace, reusable private helpers, or model a multi-step flow. Keep the public methods focused and named after domain actions.
- Use selectors for read-side queries, especially when fetching spans relations, shapes data for APIs, avoids N+1 behavior, or centralizes non-trivial query composition.
- Keep serializers at the interface boundary. Use them for parsing, validating request shape, and serializing response shape; call services and selectors for behavior and data retrieval.
- Prefer simple `APIView` classes or function-based views when they make request flow explicit. Be cautious with generic views and viewsets once behavior moves beyond straightforward CRUD.
- Put simple validation based on one model's non-relational fields in `clean` or database constraints. Move validation to services when it spans relations, needs extra queries, or belongs to a workflow.
- Prefer database constraints when the database can enforce the invariant. Still call `full_clean()` in services so application-level validation catches problems before persistence where possible.
- Use model properties or methods only for simple calculations based on non-relational fields. Move relational, query-heavy, or complex calculations to selectors, services, or utilities.
- Design API error responses intentionally. Either lightly normalize DRF defaults or define an application error hierarchy and a consistent response envelope such as `message` plus `extra`.
- Let Django `ValidationError` mostly represent serializer or model validation failures. Use explicit application exceptions for business-rule failures when a uniform API contract needs them.
- Organize tests by code role: models, services, selectors, APIs/views, and shared factories. Name files after the thing under test.
- Test models only when they add validation, properties, or methods. Service tests should cover business flows and side effects. Selector tests should cover query behavior and shape. API tests should verify request/response behavior, permissions, status codes, and wiring to the application layer.
- Use factories for readable setup, but do not hide facts that are important to the assertion.
- Keep Celery tasks thin. Task bodies should delegate to services, handle retry/idempotency/operational concerns, and avoid becoming a second business layer.
- Treat settings and integrations as explicit edges. Prefix Django environment variables consistently, read configuration deliberately, and isolate third-party calls behind services or integration modules.

## Trigger rules

- When a view, serializer, form, or admin method starts coordinating business decisions, introduce or reuse a service and keep the interface layer humble.
- When a query appears in multiple views or serializers, or a serializer field risks N+1 behavior, move the retrieval logic into a selector.
- When model `save`, signals, managers, or querysets are used to hide workflow behavior, move the behavior to an explicit service unless the local project has a strong convention otherwise.
- When service logic writes multiple records or calls external systems, consider `transaction.atomic`, idempotency, and what can be safely retried.
- When validation errors must be returned through an API, verify that Django, DRF, and application exceptions produce the documented response shape.
- When adopting this style in an existing project, migrate incrementally around the changed feature rather than reorganizing the whole app.

## Final checklist

- Business behavior is traceable from API/view/admin/task to service to model or integration?
- Reads live in selectors when they are reusable, relational, or performance-sensitive?
- Serializers validate and transform interface data without owning domain workflows?
- Models contain only data, simple invariants, and simple derived behavior?
- Services call `full_clean()` before saving changed models where appropriate?
- Transactions, idempotency, and retries are considered for multi-step writes and tasks?
- API errors have a deliberate, consistent contract?
- Tests are organized around models, services, selectors, and APIs/views with focused assertions?
