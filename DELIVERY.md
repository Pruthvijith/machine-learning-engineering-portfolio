# Delivery report · v0.1.0 research milestone

Seven local Git repositories, including the portfolio index. Each has a local release tag. The six project rows below describe Python package statement coverage, including training and CLI code in that package. Optional external adapters and the index are tracked separately. All six main packages passed Ruff formatting, Ruff lint and mypy with untyped function bodies checked. Third-party libraries are treated as external interfaces.

| Project | Local tests | Coverage | Maturity | Git commit |
|---|---:|---:|---|---|
| industrial-foundation-model-engineering | 8 | 93.46% | Reproducible research implementation | 360fc59d59a2 |
| engineering-llm-evaluation-framework | 13 | 91.37% | Reproducible research implementation | 9ff08125d695 |
| llm-inference-performance-engineering | 5 | 90.91% | Reproducible research implementation | ff5c15c00aba |
| industrial-predictive-maintenance-ml | 5 | 89.03% | Reproducible research implementation | fe4022925443 |
| multimodal-engineering-document-intelligence | 4 | 96.61% | Reproducible research implementation | 294cc4c2e5d8 |
| sovereign-ai-mlops-platform | 3 | 85.11% | Reproducible research implementation | 8dfa53fb8269 |

The six projects passed 38 tests and the index passed three more, for **41 local tests**. Weighted core statement coverage is 91.40%. Unit, regression, interface, concurrency and end-to-end checks use real small models or explicitly identified fixtures. The offline cross-project run completed and generated [the report catalogue](reports/integrated-catalogue.json). No hosted GitHub run or public release URL has been verified.

## Experiments and release decision

| Experiment | Verified result | Primary evidence |
|---|---|---|
| SmolLM2-135M CPU adaptation | Base 8/48, SFT 13/48, DPO 14/48. A repeat produced identical adapter hashes. | Project 1, reports/run.json and repeated_run.json |
| Constrained reinforcement learning and distillation | GRPO 11/48, learned reward preference accuracy 23/48, student accuracy 11/48. | Project 1, reports/alignment.json |
| Independent evaluation | Harness confirmed 14/48. The 95% paired gain interval crossed zero. All 72 free responses failed the numeric output contract. | Project 2, reports/harness.json, base-dpo.json and numeric.json |
| Judge calibration | Chose the first candidate in every presentation. Oracle agreement 50%, kappa zero. | Project 2, reports/judge.json |
| CPU serving | FP32 vs INT8 P95 657.2 vs 207.3 ms. Quality 14/48 vs 10/48. GGUF F16 vs mixed Q4_K_M quality 14/48 vs 13/48. | Project 3, reports/cpu.json, gguf_quality.json and gguf_bench.json |
| Public energy forecasting | Next-interval MAE 26.74 Wh persistence, 25.57 Wh LSTM, 25.24 Wh TCN. | Project 4, reports/energy.json |
| Synthetic condition and retrieval | Spectral baseline beat CNN. Thermal feature baseline beat CNN. Conditional part counts beat the embedding model on Recall@5. | Project 4, reports/vibration.json, thermal.json and parts.json |
| Multimodal cards | 32/32 controlled held-out cards extracted exactly. Fixed-layout synthetic evaluation only. | Project 5, reports/cards.json |
| Release lifecycle | Actual DPO release held at testing. MLflow candidate version 1 recorded locally. Positive promotion and rollback validated on fixtures. | Project 6, reports/held-release.json and mlflow.json |

## Publication and operational limits

The GitHub account was authenticated for repository inspection. Nine existing owner-visible repositories were inspected and the requested names were distinct. The available account connection could not create repositories, the originating browser extension was unavailable, and the local GitHub CLI was unauthenticated. No existing remote repository was modified. See README.md for the archive publisher and TRACKER.md for the remaining verification work.

The final core dependency scan reported 19 advisory records across three packages. Hosted security scans are configured to surface applicable advisories. The tested environment had no Docker CLI or CUDA GPU. Larger-model settings were checked for model configuration and tokenisation only. Actual multi-node training, production deployment, human studies and external industrial validation remain open.
