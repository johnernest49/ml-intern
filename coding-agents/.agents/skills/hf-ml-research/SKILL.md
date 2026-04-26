---
name: hf-ml-research
description: Research current Hugging Face ML recipes from papers, docs, datasets, models, and working examples before implementation.
---

# HF ML Research

Use this skill before writing ML training, fine-tuning, inference, or evaluation
code where current HF APIs or task recipes matter.

## Research Order

1. Find anchor papers for the task or domain.
2. Crawl downstream citations for recent improvements.
3. Read methodology, experiments, and results sections rather than relying on
   abstracts.
4. Extract recipes that connect dataset, method, hyperparameters, and measured
   result.
5. Validate datasets on the Hub: splits, columns, sample rows, licenses, and
   format fit.
6. Validate models: repo exists, architecture, tokenizer, size, access, and
   gated/private requirements.
7. Read current implementation examples and official docs for TRL,
   Transformers, Datasets, PEFT, Accelerate, Trackio, vLLM, or other relevant
   libraries.

## Output Shape

Return a ranked set of recipes:

- Paper: title, date, venue, arXiv or URL.
- Result: exact metric and benchmark.
- Dataset: Hub ID, size, schema, and format verification.
- Method: trainer, loss, optimizer, learning rate, schedule, epochs, batch size,
  sequence length, and notable preprocessing.
- Code pattern: exact docs/example files, imports, config classes, and current
  argument names.
- Recommendation: best first implementation and known gaps.

## Common Failure Modes To Avoid

- Hallucinated imports or deprecated trainer arguments.
- Assuming dataset columns without inspection.
- Silently substituting unavailable datasets or models.
- Treating example snippets as current without checking docs.
- Reporting papers without tying results to the recipe that produced them.
