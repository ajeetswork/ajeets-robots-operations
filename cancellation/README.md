# Product operations async workflows
Inventory synchronization, product imports, preview generation, and quote refresh accept a caller AbortSignal. Gateway methods represent asynchronous remote requests and accept an optional cancellation signal. Ledger marks completion or failure; leases are held for the duration of each job. Implementations of adapters are injected by the calling service.
