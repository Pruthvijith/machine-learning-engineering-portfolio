# Security and intended use

The CPU code is a research snapshot. Keep it on an isolated local machine using the pinned, vetted public inputs. The dependency snapshot, advisories and missing deployment controls block a production release. Remote-code model loading is disabled in the benchmark and runtime weights are staged as safetensors or GGUF. Treat any newly supplied model, image parser or external binary as a dependency requiring review.

## Advisory evidence

The archive contains reports/dependency-audit.json. It records a pip-audit lookup for the installed core Linux CPU package closure, using the upstream Torch version for advisory matching. Development pytest was upgraded after the initial scan. The final core scan found 19 advisory records across three packages: eight for torch, ten for transformers and one for fsspec. Some findings have suggested fixed versions. Others have no fix listed in the scan. The reproducibility pins preserve the environment for the published measurements. Optional external evaluators, OCR binaries, container images, llama.cpp and GPU dependencies need separate review. A clean result for one component cannot qualify the deployment.

## Data, hosting and regulatory review

Original inputs are synthetic or licensed public research data. No employer data, applicant files, private correspondence or individual customer records enter these repositories. Keep access tokens and signing keys outside Git. The authenticated demo APIs bind to loopback by default in the runbooks. Transport security, external identity, rate limits, role separation, managed keys and a backup restoration exercise remain deployment work.

Before introducing real maintenance tickets or documents, identify the intended purpose, who can read the material, data minimisation, retention, evaluation ownership and human review requirements. Review GDPR scope and any EU AI Act obligations for the actual deployment with the responsible organisation. This research artifact carries no legal, security or aviation approval.

References: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng and https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng.
