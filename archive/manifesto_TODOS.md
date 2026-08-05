# Todos and Open Questions

## General and Thesis

* is using `*` to select all columns considered harmful or neutral with this pattern? (should we recommend selecting columns as a principle?)
* check that CAST is used appropriately in all examples
* call out cross-connector/multi-connector cases more?
* don't use `####` in the final version, too close to `**blah**`
* manifesto should expand on how agents need more dynamic datasets than traditional apps
* manifesto should expand on platform-specific behaviors and advice/warnings (ie PostgreSQL-specific notes, etc)
* add note about literal use of catalog names (not all catalogs that map to postgresql will actually be named 'postgresql', but we use rather literal catalog names in this document to make it clearer what backing store is being used in each example)
* how does this pattern mesh with system-level or catalog-level access controls? (may be another variation to consider)
* virtual views are compatible with materialized views as base layers, but this isn't called out (and are there any special implications?)
* security - intentionally breaking a layer can brick a whole hierarchy, oh if somehow you could rollback after bricking a whole hierarchy
* `alter view ...rename to...` isn't covered by docs or examples, does this have unique potential for swapping layers?
* all complete examples should show use of CAST since that's what we are recommending as a best practice
* view comments can be really useful for self-documenting systems, consider for cases where docs are recommended?
* having an agent to check/perform/rollback view changes would be really cool

## Principles

(none)

## Use Cases

* use case 7: show iceberg types used in base table (not shown elsewhere, examples are using 'myapp.data.logs' instead of 'myapp.logs.all', "zero application changes" should be "zero changes to existing application code", remove phase 3 (this case covered by updated use-case 3), gantt chart isn't a big help
* use case 8?
  * **The Challenge**: Database dependencies are typically hardcoded, making it difficult to handle peak loads, service outages, or cost optimization without modifying and redeploying the application.
  * **The Challenge**: Database dependencies are typically hardcoded, making it difficult to handle peak loads, service outages, or cost optimization without modifying and redeploying the application.

## Implementation

* taken out of build for now
* in complete example. switch 'ecommerce.api.orders' to 'ecommerce.orders.api', expand note on swapping hierarchy vs replacing existing views
* break out instructions for brand-new applications vs upgrading existing applications
* add notes on long-term maintenance (backing up definitions, detecting and removing orphans by renaming first)
* show environment switching in phase 3 of complete example?
* add note on how to check overhead of virtualization?
* poor man evolution with views created as chicken bits

## Pitfalls

* pitfall 6: in extreme cases, invalid configurations can prevent Trino from starting

## Anti-Patterns

* add "you're using an ORM for most data access already" as an anti-pattern
* when NOT should maybe include if schema needs to be audited or navigated with approved ERD tools -- this shouldn't be treated as a trivial concern, there is nothing to prevent ridiculously complex hierarchies from evolving (in one logical step at a time) and even a moderate number of virtual views can become difficult to manage (and ViewMapper currently only supports Trino/Starburst) open a ticket to talk about other platforms (on the verge of an advertisement here)
