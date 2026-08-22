# Routing Preflight

Run this checklist before beginning substantive execution.

1. Ethan OS has been loaded — `ethan-os/entrypoint/ethan-os.md` and the repository routing rule are active.
2. The applicable domain and workflow have been resolved from the user request.
3. The relevant schemas and instructions have been identified and loaded.
4. Required `ethan-life` state/object changes have been considered and, if needed, created or updated before downstream integration work.
5. Downstream repositories/integrations (e.g., `ethan-notion`, live Notion) have been identified.
6. Downstream implementation work does not begin before upstream `ethan-os` and `ethan-life` state is resolved.
7. If the request is a pure integration/infrastructure request (e.g., a Notion property, relation, mapping, or database ID change), the documented exception applies and the request may start in the relevant downstream repository.
