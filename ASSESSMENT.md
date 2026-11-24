# Technical assessment and interview preparation

## How to read the scores

These are evidence-completeness scores for this portfolio milestone. They do not estimate an applicant's years of experience, personal proficiency or probability of receiving an offer. Each dimension has four equally weighted checks. Score each check as 0 for absent, 0.5 for partial evidence or configuration only, and 1 for a representative executed check. Multiply the sum by 25. A reproducible training run earns implementation credit even when the model fails the quality gate.

| Dimension | Target | Four checks and earned credit | Score |
|---|---:|---|---:|
| Applied ML | 95 | Open data forecasting 1, model comparisons 1, multimodal training 1, external industrial validation 0 | 75 |
| Model evaluation and readiness | 98 | Paired independent scorer 1, explicit release decision 1, expert-calibrated human evaluation 0, sufficient domain breadth 0.5 | 62.5 |
| Engineering domain | 95 | Dimensional verification 1, physically motivated vibration features 1, observed load forecasting 1, actual industrial thermography/aircraft validation 0 | 75 |
| LLM post-training | 97 | Open-weight adapter SFT 1, DPO against SFT reference 1, bounded policy optimisation and distillation 0.5, realistic free-form engineering adaptation 0 | 62.5 |
| GPU and inference | 94 | Paired quantisation/quality benchmark 1, concurrent CPU/engine measurements 1, on-prem GPU serving 0, distributed training benchmark 0 | 50 |
| Software engineering quality | 96 | Automated contract and integration tests 1, static checks 1, versioned reproducible artifacts 1, independently reviewed/security-qualified dependencies 0 | 75 |
| Reproducibility | 98 | Immutable upstream inputs 1, repeatable training digests 1, machine-readable outputs 1, clean-room external replication 0 | 75 |
| Documentation | 98 | Run commands and data provenance 1, limitations and case-level results 1, design and interview guides 1, independent documentation usability test 0 | 75 |
| Production maturity | 95 | Offline integration on a real candidate 1, promotion controls and fixture rollback 0.5, real user operations 0, production security and reliability validation 0 | 37.5 |

## Recruiter and hiring-manager interpretation

Lead with the end-to-end handover. A small model was adapted, a separate evaluator rejected it, precision changes introduced measurable accuracy loss, and the model registry preserved the hold. The open checkpoint, actual failures, comparable workloads and replayable hashes distinguish this work from a notebook that only reports training loss.

For an Airbus model-development application this supports a technical work sample in model adaptation, domain evaluation and local inference. The open role also asks for years of hands-on model shipping. The evidence here supports a discussion about implementing and debugging a pipeline. Your historical employment, customer delivery, professional decisions, degrees and languages need distinct evidence. Avoid quoting adoption, analyst hours saved, A100 usage, human kappa, uplift or 70B distillation from the hypothetical CV.

The largest remaining gaps are engineering task breadth, externally labelled industrial data, multimodal generative post-training and measured GPU/distributed operation. The suite is a reproducible research implementation. It does not validate customer impact, availability, long-term drift, regulatory status or a performance service-level objective. A credible application can link the portfolio as independent AI-assisted project work. A shortlist probability cannot be inferred from these experiments.

## Personal mastery roadmap

| Order | Independent task | Observable evidence |
|---|---|---|
| 1 | Reproduce CPU training and both evaluation interfaces from clean checkouts. | Compare input digests and the two adapter hashes. Explain any difference before reporting scores. |
| 2 | Derive the single-token SFT loss, DPO log-ratio and GRPO advantage on paper. | Compute one preference pair by hand and predict the gradient direction. Explain the zero-variance group case. |
| 3 | Investigate every held-out missing-information failure and manually grade 12 raw arithmetic answers. | Separate parsing failure from calculation failure. Document one evaluator change and the bias it introduces. |
| 4 | Write a new independently authored heat-transfer benchmark and a calibration split. | Freeze the split, threshold and baseline before training. Keep the original 48-case test out of tuning. |
| 5 | Repeat inference benchmarks at three context lengths and concurrency levels. | Report warm-up, ordering, TTFT, token gaps, throughput, confidence and memory separately. |
| 6 | Run one authorised GPU profile on available hardware. | Record driver, CUDA, VRAM, precision, model revision and loss. Compare full precision and quantised results on identical inputs. |
| 7 | Exercise the lifecycle with a second signer and a simulated failed deployment. | Demonstrate staging denial, rollback and restored-service verification using a fresh database. |
| 8 | Explain this implementation without notes and modify one meaningful component. | Show the commit, failed test, correction, measurement and trade-off in a five-minute review. |

## Questions to expect

- What prevents the 48 test examples from becoming a tuning set, and how independent are their 12 groups?
- Why does the model hold even though DPO improves aggregate accuracy? Which single additional data collection would most change that decision?
- Why did the judge achieve 50% agreement and zero kappa? Could a human reviewer disagree with the equation oracle for a good reason?
- How can a compressed model be faster and still be a worse deployment choice? Which measurements reflect queueing?
- What exactly does the registry signature authenticate? Which actor could still forge a release?
- Which changes would you make first for a real aircraft-engineering corpus, and which approvals, data rights and independent validations would be required?

Each project has a separate interview guide with answers grounded in its own measurements.
