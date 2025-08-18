# 24 Architecture-Aware BO/HPO Questions (with Step-by-Step Answers) — v3
This pack adds **neural architecture** (e.g., LeNet5, ResNet*, LSTM, BERT, GPT-like) as a categorical variable and ties it to
typical optimizer/regularization preferences.

- **Q1–Q12 (GP)**: Architecture and optimizer are **fixed** per item, search space has only **continuous** dims: lr (log-real), weight_decay, dropout.

- **Q13–Q24 (TPE)**: Architecture, optimizer, and FL aggregator are **categorical**; continuous dims include lr, batch, epochs (and mu if fedprox).

Objective: **minimize** validation loss.