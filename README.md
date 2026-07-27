# Zazhytskyi_nosql_2

## Частина 1 — Підготовка даних і вибір інструментів

###  1.1. Завантаження і підготовка датасету

![Результат](screenshots/1.1.png)

### 1.2. Вибір інструментів

1. Pinecone використовує Serverless-архітектуру як основний спосіб розгортання, на відміну від self-hosted і
вбудованої бібліотеки у випадку Qdrant і Chroma відповідно.
Pinecone є комерційним (proprietary, closed-source) продуктом, сервіс надається як DBaaS (Database as a Service),
самостійно розгорнути Pinecone на власному сервері не можна (виняток — спеціальна пропозиція BYOC для великих корпоративних клієнтів, де сервіс працює у вашому хмарному акаунті). Існують тарифні плани.
Продуктивність Pinecone аналогічна Qdrant і краща ніж в Chroma.
Pinecone обирати коли: хочете зосередитися на бізнес-логіці, а не на DevOps, потрібен швидкий MVP або proof-of-concept, команда невелика, немає виділеного інфраструктурного інженера.
Qdrant обирати коли: дані не можуть покидати вашу інфраструктуру (compliance, безпека), потрібен гібридний пошук з коробки, важлива продуктивність при складних фільтрах за метаданими.
Chroma обирати коли: потрібний швидкісий старт, прототипи, експерименти, локальні RAG-пайплайни.

2. Для задачі пошуку по науковим текстам обрана модель specter2_base тому що модель specter2_base
натренована на наукових текстах.
Model Description
SPECTER2 has been trained on over 6M triplets of scientific paper citations, which are available here. Post that it is trained with additionally attached task format specific adapter modules on all the SciRepEval training tasks.
Task Formats trained on:
Classification
Regression
Proximity (Retrieval)
Adhoc Search
It builds on the work done in SciRepEval: A Multi-Format Benchmark for Scientific Document Representations and we evaluate the trained model on this benchmark as well.

3. У Model Card для allenai/specter2_base не вказано явної рекомендації щодо метрики схожості.
Метрика схожості важлива при створенні індексу. Під час створення векторного індексу необхідно заздалегідь вибрати метрику відстані, оскільки саме вона визначає, як система буде шукати найближчі вектори.


### 1.3. Отримання ембеддингів

![Результат](screenshots/1.3.png)

Тому що для нормалізованих векторів скалярний добуткок (dot product) чисельно дорівнює косинусній схожості.
Тобто при нормалізації довжина векторів стає одиничною, тому знаменник в формулі косинусної схожості стає
рівним 1, у результаті косинусна схожість і скалярний добуток мають одакове значення. 

## Частина 2 — Завантаження даних і метадані

![Результат](screenshots/2.1.png)
![Результат](screenshots/2.2.png)

## Частина 3 — Пошукові запити

```
Чистий семантичний пошук, результати:

title: Artificial Intelligence Generated Coins for Size Comparison
category: cs.CV
year: 2023.0
abstract: Authors of scientific articles use coins in photographs as a size reference
for objects. For this purpose, coins are placed next to objects when taking the
photo. In this letter we propose a novel method that uses artificial
intelligence (AI) generated images of coins to provide a size reference in
photos. The newest generation is able to quickly generate realistic
high-quality images from textual descriptions. With the proposed method no
physical coin is required while taking photos. Coins can 
------------------------------
title: Searching for Uncollected Litter with Computer Vision
category: cs.CV
year: 2022.0
abstract: This study combines photo metadata and computer vision to quantify where
uncollected litter is present. Images from the Trash Annotations in Context
(TACO) dataset were used to teach an algorithm to detect 10 categories of
garbage. Although it worked well with smartphone photos, it struggled when
trying to process images from vehicle mounted cameras. However, increasing the
variety of perspectives and backgrounds in the dataset will help it improve in
unfamiliar situations. These data are plotte
------------------------------
title: Memory and attention in deep learning
category: cs.LG
year: 2021.0
abstract: Intelligence necessitates memory. Without memory, humans fail to perform
various nontrivial tasks such as reading novels, playing games or solving
maths. As the ultimate goal of machine learning is to derive intelligent
systems that learn and act automatically just like human, memory construction
for machine is inevitable. Artificial neural networks model neurons and
synapses in the brain by interconnecting computational units via weights, which
is a typical class of machine learning algorithms 
------------------------------
title: Exploration and Exploitation in Visuomotor Prediction of Autonomous
  Agents
category: cs.LG
year: 2013.0
abstract: This paper discusses various techniques to let an agent learn how to predict
the effects of its own actions on its sensor data autonomously, and their
usefulness to apply them to visual sensors. An Extreme Learning Machine is used
for visuomotor prediction, while various autonomous control techniques that can
aid the prediction process by balancing exploration and exploitation are
discussed and tested in a simple system: a camera moving over a 2D greyscale
image.
------------------------------
title: Enhancing Pollinator Conservation towards Agriculture 4.0: Monitoring of
  Bees through Object Recognition
category: cs.CV
year: 2024.0
abstract: In an era of rapid climate change and its adverse effects on food production,
technological intervention to monitor pollinator conservation is of paramount
importance for environmental monitoring and conservation for global food
security. The survival of the human species depends on the conservation of
pollinators. This article explores the use of Computer Vision and Object
Recognition to autonomously track and report bee behaviour from images. A novel
dataset of 9664 images containing bees is e
------------------------------


Пошук з фільтрацією, приклад A, результати:

title: Robust In-Context Reinforcement Learning Under Reward Poisoning Attacks
category: cs.LG
year: 2025.0
abstract: We study the corruption-robustness of in-context reinforcement learning (ICRL), focusing on the Decision-Pretrained Transformer (DPT, Lee et al., 2023). To address the challenge of reward poisoning attacks targeting the DPT, we propose a novel adversarial training framework, called Adversarially Trained DPT (AT-DPT). Our method simultaneously trains a population of attackers to minimize the true reward of the DPT by poisoning environment rewards, and a DPT model to infer optimal actions from the
------------------------------
title: Agent-Centric Representations for Multi-Agent Reinforcement Learning
category: cs.LG
year: 2021.0
abstract: Object-centric representations have recently enabled significant progress in
tackling relational reasoning tasks. By building a strong object-centric
inductive bias into neural architectures, recent efforts have improved
generalization and data efficiency of machine learning algorithms for these
problems. One problem class involving relational reasoning that still remains
under-explored is multi-agent reinforcement learning (MARL). Here we
investigate whether object-centric representations are a
------------------------------
title: Reinforcement Learning with Fast and Forgetful Memory
category: cs.LG
year: 2023.0
abstract: Nearly all real world tasks are inherently partially observable,
necessitating the use of memory in Reinforcement Learning (RL). Most model-free
approaches summarize the trajectory into a latent Markov state using memory
models borrowed from Supervised Learning (SL), even though RL tends to exhibit
different training and efficiency characteristics. Addressing this discrepancy,
we introduce Fast and Forgetful Memory, an algorithm-agnostic memory model
designed specifically for RL. Our approach co
------------------------------
title: Improve Value Estimation of Q Function and Reshape Reward with Monte
  Carlo Tree Search
category: cs.LG
year: 2024.0
abstract: Reinforcement learning has achieved remarkable success in perfect information
games such as Go and Atari, enabling agents to compete at the highest levels
against human players. However, research in reinforcement learning for
imperfect information games has been relatively limited due to the more complex
game structures and randomness. Traditional methods face challenges in training
and improving performance in imperfect information games due to issues like
inaccurate Q value estimation and rewa
------------------------------
title: Task-specific Subnetwork Discovery in Reinforcement Learning for Autonomous Underwater Navigation
category: cs.LG
year: 2026.0
abstract: Autonomous underwater vehicles are required to perform multiple tasks adaptively and in an explainable manner under dynamic, uncertain conditions and limited sensing, challenges that classical controllers struggle to address. This demands robust, generalizable, and inherently interpretable control policies for reliable long-term monitoring. Reinforcement learning, particularly multi-task RL, overcomes these limitations by leveraging shared representations to enable efficient adaptation across ta
------------------------------


Пошук з фільтрацією, приклад B, результати:

title: Adaptive Bases for Reinforcement Learning
category: cs.LG
year: 2010.0
abstract: We consider the problem of reinforcement learning using function
approximation, where the approximating basis can change dynamically while
interacting with the environment. A motivation for such an approach is
maximizing the value function fitness to the problem faced. Three errors are
considered: approximation square error, Bellman residual, and projected Bellman
residual. Algorithms under the actor-critic framework are presented, and shown
to converge. The advantage of such an adaptive basis i
------------------------------
title: Many-body approach to the dynamics of batch learning
category: cond-mat.dis-nn
year: 1999.0
abstract: Using the cavity method and diagrammatic methods, we model the dynamics of
batch learning of restricted sets of examples, widely applicable to general
learning cost functions, and fully taking into account the temporal
correlations introduced by the recycling of the examples.
------------------------------
title: A mu-differentiable Lagrange multiplier rule
category: math.CA
year: 2008.0
abstract: We present some properties of the gradient of a mu-differentiable function.
The Method of Lagrange Multipliers for mu-differentiable functions is then
exemplified.
------------------------------
title: Exploration and Exploitation in Visuomotor Prediction of Autonomous
  Agents
category: cs.LG
year: 2013.0
abstract: This paper discusses various techniques to let an agent learn how to predict
the effects of its own actions on its sensor data autonomously, and their
usefulness to apply them to visual sensors. An Extreme Learning Machine is used
for visuomotor prediction, while various autonomous control techniques that can
aid the prediction process by balancing exploration and exploitation are
discussed and tested in a simple system: a camera moving over a 2D greyscale
image.
------------------------------
title: Linear and Geometric Mixtures - Analysis
category: cs.IT
year: 2013.0
abstract: Linear and geometric mixtures are two methods to combine arbitrary models in
data compression. Geometric mixtures generalize the empirically well-performing
PAQ7 mixture. Both mixture schemes rely on weight vectors, which heavily
determine their performance. Typically weight vectors are identified via Online
Gradient Descent. In this work we show that one can obtain strong code length
bounds for such a weight estimation scheme. These bounds hold for arbitrary
input sequences. For this purpose we
------------------------------

Top-5 статей для метрики cosine similarity:
score: 0.8357
title: Continual Reinforcement Learning deployed in Real-life using Policy
  Distillation and Sim2Real Transfer, abstract: We focus on the problem of teaching a robot to solve tasks presented
sequentially, i.e., in a continual learning scenario. The robot should be able
to solve all tasks it has encountered, without forgetting past tasks. We
provide preliminary work on applying Reinforcement Learning to such setting, on
2D navigation tasks for a 3 wheel omni-directional robot. Our approach takes
advantage of state representation learning and policy distillation. Policies
are trained using learned features as input, rather than raw observations,
allowing better sample efficiency. Policy distillation is used to combine
multiple policies into a single one that solves all encountered tasks.
abstract: We focus on the problem of teaching a robot to solve tasks presented
sequentially, i.e., in a continual learning scenario. The robot should be able
to solve all tasks it has encountered, without forgetting past tasks. We
provide preliminary work on applying Reinforcement Learning to such setting, on
2D navigation tasks for a 3 wheel omni-directional robot. Our approach takes
advantage of state representation learning and policy distillation. Policies
are trained using learned features as input, rather than raw observations,
allowing better sample efficiency. Policy distillation is used to combine
multiple policies into a single one that solves all encountered tasks.
------------------------------
score: 0.8276
title: UAV Trajectory Optimization via Improved Noisy Deep Q-Network, abstract: This paper proposes an Improved Noisy Deep Q-Network (Noisy DQN) to enhance the exploration and stability of Unmanned Aerial Vehicle (UAV) when applying deep reinforcement learning in simulated environments. This method enhances the exploration ability by combining the residual NoisyLinear layer with an adaptive noise scheduling mechanism, while improving training stability through smooth loss and soft target network updates. Experiments show that the proposed model achieves faster convergence and up to $+40$ higher rewards compared to standard DQN and quickly reach to the minimum number of steps required for the task 28 in the 15 * 15 grid navigation environment set up. The results show that our comprehensive improvements to the network structure of NoisyNet, exploration control, and training stability contribute to enhancing the efficiency and reliability of deep Q-learning.
abstract: This paper proposes an Improved Noisy Deep Q-Network (Noisy DQN) to enhance the exploration and stability of Unmanned Aerial Vehicle (UAV) when applying deep reinforcement learning in simulated environments. This method enhances the exploration ability by combining the residual NoisyLinear layer with an adaptive noise scheduling mechanism, while improving training stability through smooth loss and soft target network updates. Experiments show that the proposed model achieves faster convergence and up to $+40$ higher rewards compared to standard DQN and quickly reach to the minimum number of steps required for the task 28 in the 15 * 15 grid navigation environment set up. The results show that our comprehensive improvements to the network structure of NoisyNet, exploration control, and training stability contribute to enhancing the efficiency and reliability of deep Q-learning.
------------------------------
score: 0.8248
title: Robust In-Context Reinforcement Learning Under Reward Poisoning Attacks, abstract: We study the corruption-robustness of in-context reinforcement learning (ICRL), focusing on the Decision-Pretrained Transformer (DPT, Lee et al., 2023). To address the challenge of reward poisoning attacks targeting the DPT, we propose a novel adversarial training framework, called Adversarially Trained DPT (AT-DPT). Our method simultaneously trains a population of attackers to minimize the true reward of the DPT by poisoning environment rewards, and a DPT model to infer optimal actions from the poisoned data. We evaluate the effectiveness of our approach against standard bandit algorithms, including robust baselines designed to handle reward contamination. Our results show that AT-DPT significantly outperforms them in bandit settings under a learned attacker, and generalizes to more complex environments such as adaptive attackers and MDPs. It shows promise in ICRL as a meta-RL approach to learning effective corruption-robust algorithms.
abstract: We study the corruption-robustness of in-context reinforcement learning (ICRL), focusing on the Decision-Pretrained Transformer (DPT, Lee et al., 2023). To address the challenge of reward poisoning attacks targeting the DPT, we propose a novel adversarial training framework, called Adversarially Trained DPT (AT-DPT). Our method simultaneously trains a population of attackers to minimize the true reward of the DPT by poisoning environment rewards, and a DPT model to infer optimal actions from the poisoned data. We evaluate the effectiveness of our approach against standard bandit algorithms, including robust baselines designed to handle reward contamination. Our results show that AT-DPT significantly outperforms them in bandit settings under a learned attacker, and generalizes to more complex environments such as adaptive attackers and MDPs. It shows promise in ICRL as a meta-RL approach to learning effective corruption-robust algorithms.
------------------------------
score: 0.8240
title: Adaptive Bases for Reinforcement Learning, abstract: We consider the problem of reinforcement learning using function
approximation, where the approximating basis can change dynamically while
interacting with the environment. A motivation for such an approach is
maximizing the value function fitness to the problem faced. Three errors are
considered: approximation square error, Bellman residual, and projected Bellman
residual. Algorithms under the actor-critic framework are presented, and shown
to converge. The advantage of such an adaptive basis is demonstrated in
simulations.
abstract: We consider the problem of reinforcement learning using function
approximation, where the approximating basis can change dynamically while
interacting with the environment. A motivation for such an approach is
maximizing the value function fitness to the problem faced. Three errors are
considered: approximation square error, Bellman residual, and projected Bellman
residual. Algorithms under the actor-critic framework are presented, and shown
to converge. The advantage of such an adaptive basis is demonstrated in
simulations.
------------------------------
score: 0.8238
title: Agent-Centric Representations for Multi-Agent Reinforcement Learning, abstract: Object-centric representations have recently enabled significant progress in
tackling relational reasoning tasks. By building a strong object-centric
inductive bias into neural architectures, recent efforts have improved
generalization and data efficiency of machine learning algorithms for these
problems. One problem class involving relational reasoning that still remains
under-explored is multi-agent reinforcement learning (MARL). Here we
investigate whether object-centric representations are also beneficial in the
fully cooperative MARL setting. Specifically, we study two ways of
incorporating an agent-centric inductive bias into our RL algorithm: 1.
Introducing an agent-centric attention module with explicit connections across
agents 2. Adding an agent-centric unsupervised predictive objective (i.e. not
using action labels), to be used as an auxiliary loss for MARL, or as the basis
of a pre-training step. We evaluate these approaches on the Google Research
Football environment as well as DeepMind Lab 2D. Empirically, agent-centric
representation learning leads to the emergence of more complex cooperation
strategies between agents as well as enhanced sample efficiency and
generalization.
abstract: Object-centric representations have recently enabled significant progress in
tackling relational reasoning tasks. By building a strong object-centric
inductive bias into neural architectures, recent efforts have improved
generalization and data efficiency of machine learning algorithms for these
problems. One problem class involving relational reasoning that still remains
under-explored is multi-agent reinforcement learning (MARL). Here we
investigate whether object-centric representations are also beneficial in the
fully cooperative MARL setting. Specifically, we study two ways of
incorporating an agent-centric inductive bias into our RL algorithm: 1.
Introducing an agent-centric attention module with explicit connections across
agents 2. Adding an agent-centric unsupervised predictive objective (i.e. not
using action labels), to be used as an auxiliary loss for MARL, or as the basis
of a pre-training step. We evaluate these approaches on the Google Research
Football environment as well as DeepMind Lab 2D. Empirically, agent-centric
representation learning leads to the emergence of more complex cooperation
strategies between agents as well as enhanced sample efficiency and
generalization.
------------------------------

Top-5 статей для метрики dot product:
score: 0.8357
title: Continual Reinforcement Learning deployed in Real-life using Policy
  Distillation and Sim2Real Transfer, abstract: We focus on the problem of teaching a robot to solve tasks presented
sequentially, i.e., in a continual learning scenario. The robot should be able
to solve all tasks it has encountered, without forgetting past tasks. We
provide preliminary work on applying Reinforcement Learning to such setting, on
2D navigation tasks for a 3 wheel omni-directional robot. Our approach takes
advantage of state representation learning and policy distillation. Policies
are trained using learned features as input, rather than raw observations,
allowing better sample efficiency. Policy distillation is used to combine
multiple policies into a single one that solves all encountered tasks.
abstract: We focus on the problem of teaching a robot to solve tasks presented
sequentially, i.e., in a continual learning scenario. The robot should be able
to solve all tasks it has encountered, without forgetting past tasks. We
provide preliminary work on applying Reinforcement Learning to such setting, on
2D navigation tasks for a 3 wheel omni-directional robot. Our approach takes
advantage of state representation learning and policy distillation. Policies
are trained using learned features as input, rather than raw observations,
allowing better sample efficiency. Policy distillation is used to combine
multiple policies into a single one that solves all encountered tasks.
------------------------------
score: 0.8276
title: UAV Trajectory Optimization via Improved Noisy Deep Q-Network, abstract: This paper proposes an Improved Noisy Deep Q-Network (Noisy DQN) to enhance the exploration and stability of Unmanned Aerial Vehicle (UAV) when applying deep reinforcement learning in simulated environments. This method enhances the exploration ability by combining the residual NoisyLinear layer with an adaptive noise scheduling mechanism, while improving training stability through smooth loss and soft target network updates. Experiments show that the proposed model achieves faster convergence and up to $+40$ higher rewards compared to standard DQN and quickly reach to the minimum number of steps required for the task 28 in the 15 * 15 grid navigation environment set up. The results show that our comprehensive improvements to the network structure of NoisyNet, exploration control, and training stability contribute to enhancing the efficiency and reliability of deep Q-learning.
abstract: This paper proposes an Improved Noisy Deep Q-Network (Noisy DQN) to enhance the exploration and stability of Unmanned Aerial Vehicle (UAV) when applying deep reinforcement learning in simulated environments. This method enhances the exploration ability by combining the residual NoisyLinear layer with an adaptive noise scheduling mechanism, while improving training stability through smooth loss and soft target network updates. Experiments show that the proposed model achieves faster convergence and up to $+40$ higher rewards compared to standard DQN and quickly reach to the minimum number of steps required for the task 28 in the 15 * 15 grid navigation environment set up. The results show that our comprehensive improvements to the network structure of NoisyNet, exploration control, and training stability contribute to enhancing the efficiency and reliability of deep Q-learning.
------------------------------
score: 0.8248
title: Robust In-Context Reinforcement Learning Under Reward Poisoning Attacks, abstract: We study the corruption-robustness of in-context reinforcement learning (ICRL), focusing on the Decision-Pretrained Transformer (DPT, Lee et al., 2023). To address the challenge of reward poisoning attacks targeting the DPT, we propose a novel adversarial training framework, called Adversarially Trained DPT (AT-DPT). Our method simultaneously trains a population of attackers to minimize the true reward of the DPT by poisoning environment rewards, and a DPT model to infer optimal actions from the poisoned data. We evaluate the effectiveness of our approach against standard bandit algorithms, including robust baselines designed to handle reward contamination. Our results show that AT-DPT significantly outperforms them in bandit settings under a learned attacker, and generalizes to more complex environments such as adaptive attackers and MDPs. It shows promise in ICRL as a meta-RL approach to learning effective corruption-robust algorithms.
abstract: We study the corruption-robustness of in-context reinforcement learning (ICRL), focusing on the Decision-Pretrained Transformer (DPT, Lee et al., 2023). To address the challenge of reward poisoning attacks targeting the DPT, we propose a novel adversarial training framework, called Adversarially Trained DPT (AT-DPT). Our method simultaneously trains a population of attackers to minimize the true reward of the DPT by poisoning environment rewards, and a DPT model to infer optimal actions from the poisoned data. We evaluate the effectiveness of our approach against standard bandit algorithms, including robust baselines designed to handle reward contamination. Our results show that AT-DPT significantly outperforms them in bandit settings under a learned attacker, and generalizes to more complex environments such as adaptive attackers and MDPs. It shows promise in ICRL as a meta-RL approach to learning effective corruption-robust algorithms.
------------------------------
score: 0.8240
title: Adaptive Bases for Reinforcement Learning, abstract: We consider the problem of reinforcement learning using function
approximation, where the approximating basis can change dynamically while
interacting with the environment. A motivation for such an approach is
maximizing the value function fitness to the problem faced. Three errors are
considered: approximation square error, Bellman residual, and projected Bellman
residual. Algorithms under the actor-critic framework are presented, and shown
to converge. The advantage of such an adaptive basis is demonstrated in
simulations.
abstract: We consider the problem of reinforcement learning using function
approximation, where the approximating basis can change dynamically while
interacting with the environment. A motivation for such an approach is
maximizing the value function fitness to the problem faced. Three errors are
considered: approximation square error, Bellman residual, and projected Bellman
residual. Algorithms under the actor-critic framework are presented, and shown
to converge. The advantage of such an adaptive basis is demonstrated in
simulations.
------------------------------
score: 0.8238
title: Agent-Centric Representations for Multi-Agent Reinforcement Learning, abstract: Object-centric representations have recently enabled significant progress in
tackling relational reasoning tasks. By building a strong object-centric
inductive bias into neural architectures, recent efforts have improved
generalization and data efficiency of machine learning algorithms for these
problems. One problem class involving relational reasoning that still remains
under-explored is multi-agent reinforcement learning (MARL). Here we
investigate whether object-centric representations are also beneficial in the
fully cooperative MARL setting. Specifically, we study two ways of
incorporating an agent-centric inductive bias into our RL algorithm: 1.
Introducing an agent-centric attention module with explicit connections across
agents 2. Adding an agent-centric unsupervised predictive objective (i.e. not
using action labels), to be used as an auxiliary loss for MARL, or as the basis
of a pre-training step. We evaluate these approaches on the Google Research
Football environment as well as DeepMind Lab 2D. Empirically, agent-centric
representation learning leads to the emergence of more complex cooperation
strategies between agents as well as enhanced sample efficiency and
generalization.
abstract: Object-centric representations have recently enabled significant progress in
tackling relational reasoning tasks. By building a strong object-centric
inductive bias into neural architectures, recent efforts have improved
generalization and data efficiency of machine learning algorithms for these
problems. One problem class involving relational reasoning that still remains
under-explored is multi-agent reinforcement learning (MARL). Here we
investigate whether object-centric representations are also beneficial in the
fully cooperative MARL setting. Specifically, we study two ways of
incorporating an agent-centric inductive bias into our RL algorithm: 1.
Introducing an agent-centric attention module with explicit connections across
agents 2. Adding an agent-centric unsupervised predictive objective (i.e. not
using action labels), to be used as an auxiliary loss for MARL, or as the basis
of a pre-training step. We evaluate these approaches on the Google Research
Football environment as well as DeepMind Lab 2D. Empirically, agent-centric
representation learning leads to the emergence of more complex cooperation
strategies between agents as well as enhanced sample efficiency and
generalization.
------------------------------

Top-5 статей для метрики L2-distance distance:
score: 0.5733
title: Continual Reinforcement Learning deployed in Real-life using Policy
  Distillation and Sim2Real Transfer, abstract: We focus on the problem of teaching a robot to solve tasks presented
sequentially, i.e., in a continual learning scenario. The robot should be able
to solve all tasks it has encountered, without forgetting past tasks. We
provide preliminary work on applying Reinforcement Learning to such setting, on
2D navigation tasks for a 3 wheel omni-directional robot. Our approach takes
advantage of state representation learning and policy distillation. Policies
are trained using learned features as input, rather than raw observations,
allowing better sample efficiency. Policy distillation is used to combine
multiple policies into a single one that solves all encountered tasks.
abstract: We focus on the problem of teaching a robot to solve tasks presented
sequentially, i.e., in a continual learning scenario. The robot should be able
to solve all tasks it has encountered, without forgetting past tasks. We
provide preliminary work on applying Reinforcement Learning to such setting, on
2D navigation tasks for a 3 wheel omni-directional robot. Our approach takes
advantage of state representation learning and policy distillation. Policies
are trained using learned features as input, rather than raw observations,
allowing better sample efficiency. Policy distillation is used to combine
multiple policies into a single one that solves all encountered tasks.
------------------------------
score: 0.5872
title: UAV Trajectory Optimization via Improved Noisy Deep Q-Network, abstract: This paper proposes an Improved Noisy Deep Q-Network (Noisy DQN) to enhance the exploration and stability of Unmanned Aerial Vehicle (UAV) when applying deep reinforcement learning in simulated environments. This method enhances the exploration ability by combining the residual NoisyLinear layer with an adaptive noise scheduling mechanism, while improving training stability through smooth loss and soft target network updates. Experiments show that the proposed model achieves faster convergence and up to $+40$ higher rewards compared to standard DQN and quickly reach to the minimum number of steps required for the task 28 in the 15 * 15 grid navigation environment set up. The results show that our comprehensive improvements to the network structure of NoisyNet, exploration control, and training stability contribute to enhancing the efficiency and reliability of deep Q-learning.
abstract: This paper proposes an Improved Noisy Deep Q-Network (Noisy DQN) to enhance the exploration and stability of Unmanned Aerial Vehicle (UAV) when applying deep reinforcement learning in simulated environments. This method enhances the exploration ability by combining the residual NoisyLinear layer with an adaptive noise scheduling mechanism, while improving training stability through smooth loss and soft target network updates. Experiments show that the proposed model achieves faster convergence and up to $+40$ higher rewards compared to standard DQN and quickly reach to the minimum number of steps required for the task 28 in the 15 * 15 grid navigation environment set up. The results show that our comprehensive improvements to the network structure of NoisyNet, exploration control, and training stability contribute to enhancing the efficiency and reliability of deep Q-learning.
------------------------------
score: 0.5920
title: Robust In-Context Reinforcement Learning Under Reward Poisoning Attacks, abstract: We study the corruption-robustness of in-context reinforcement learning (ICRL), focusing on the Decision-Pretrained Transformer (DPT, Lee et al., 2023). To address the challenge of reward poisoning attacks targeting the DPT, we propose a novel adversarial training framework, called Adversarially Trained DPT (AT-DPT). Our method simultaneously trains a population of attackers to minimize the true reward of the DPT by poisoning environment rewards, and a DPT model to infer optimal actions from the poisoned data. We evaluate the effectiveness of our approach against standard bandit algorithms, including robust baselines designed to handle reward contamination. Our results show that AT-DPT significantly outperforms them in bandit settings under a learned attacker, and generalizes to more complex environments such as adaptive attackers and MDPs. It shows promise in ICRL as a meta-RL approach to learning effective corruption-robust algorithms.
abstract: We study the corruption-robustness of in-context reinforcement learning (ICRL), focusing on the Decision-Pretrained Transformer (DPT, Lee et al., 2023). To address the challenge of reward poisoning attacks targeting the DPT, we propose a novel adversarial training framework, called Adversarially Trained DPT (AT-DPT). Our method simultaneously trains a population of attackers to minimize the true reward of the DPT by poisoning environment rewards, and a DPT model to infer optimal actions from the poisoned data. We evaluate the effectiveness of our approach against standard bandit algorithms, including robust baselines designed to handle reward contamination. Our results show that AT-DPT significantly outperforms them in bandit settings under a learned attacker, and generalizes to more complex environments such as adaptive attackers and MDPs. It shows promise in ICRL as a meta-RL approach to learning effective corruption-robust algorithms.
------------------------------
score: 0.5933
title: Adaptive Bases for Reinforcement Learning, abstract: We consider the problem of reinforcement learning using function
approximation, where the approximating basis can change dynamically while
interacting with the environment. A motivation for such an approach is
maximizing the value function fitness to the problem faced. Three errors are
considered: approximation square error, Bellman residual, and projected Bellman
residual. Algorithms under the actor-critic framework are presented, and shown
to converge. The advantage of such an adaptive basis is demonstrated in
simulations.
abstract: We consider the problem of reinforcement learning using function
approximation, where the approximating basis can change dynamically while
interacting with the environment. A motivation for such an approach is
maximizing the value function fitness to the problem faced. Three errors are
considered: approximation square error, Bellman residual, and projected Bellman
residual. Algorithms under the actor-critic framework are presented, and shown
to converge. The advantage of such an adaptive basis is demonstrated in
simulations.
------------------------------
score: 0.5937
title: Agent-Centric Representations for Multi-Agent Reinforcement Learning, abstract: Object-centric representations have recently enabled significant progress in
tackling relational reasoning tasks. By building a strong object-centric
inductive bias into neural architectures, recent efforts have improved
generalization and data efficiency of machine learning algorithms for these
problems. One problem class involving relational reasoning that still remains
under-explored is multi-agent reinforcement learning (MARL). Here we
investigate whether object-centric representations are also beneficial in the
fully cooperative MARL setting. Specifically, we study two ways of
incorporating an agent-centric inductive bias into our RL algorithm: 1.
Introducing an agent-centric attention module with explicit connections across
agents 2. Adding an agent-centric unsupervised predictive objective (i.e. not
using action labels), to be used as an auxiliary loss for MARL, or as the basis
of a pre-training step. We evaluate these approaches on the Google Research
Football environment as well as DeepMind Lab 2D. Empirically, agent-centric
representation learning leads to the emergence of more complex cooperation
strategies between agents as well as enhanced sample efficiency and
generalization.
abstract: Object-centric representations have recently enabled significant progress in
tackling relational reasoning tasks. By building a strong object-centric
inductive bias into neural architectures, recent efforts have improved
generalization and data efficiency of machine learning algorithms for these
problems. One problem class involving relational reasoning that still remains
under-explored is multi-agent reinforcement learning (MARL). Here we
investigate whether object-centric representations are also beneficial in the
fully cooperative MARL setting. Specifically, we study two ways of
incorporating an agent-centric inductive bias into our RL algorithm: 1.
Introducing an agent-centric attention module with explicit connections across
agents 2. Adding an agent-centric unsupervised predictive objective (i.e. not
using action labels), to be used as an auxiliary loss for MARL, or as the basis
of a pre-training step. We evaluate these approaches on the Google Research
Football environment as well as DeepMind Lab 2D. Empirically, agent-centric
representation learning leads to the emergence of more complex cooperation
strategies between agents as well as enhanced sample efficiency and
generalization.
------------------------------
```

Хоча у випадку обох прикладів А та В пошук був проведений за запитом "reinforcement learning", результати пошуку відрізняються, тому що пошук проводився з фільтрацією результатів. В першому випадку в рекзультат попали статті за останні 5 років і категорії cs.LG, а в другому випадку в рекзультат попали статті до 2015 року будь-якої категорії.

1. Результати топ-5 для cosine і dot product збігаються тому що для нормалізованих векторів скалярний добуткок чисельно дорівнює косинусній схожості.
2. Результати для L2 не відрізняються тому що вектори нормалізовані.
3. Якби ембеддинги не були нормалізовані тоді довжини векторів були б різні, довжина вектора впливала б на результат розрахунку dot product і L2-distance і результати були б незавжди еквівалентні.

## Частина 4 — Chunking

1. Розбивка тексту на чанки за стратегією Semantic chunking дає більш осмислені чанки, так як чанк містить цілі речення.
2. У випадку Fixed-size chunking є випадки розрізаних речень. Зміст чанку може бути неповним і спотвореним.
3. При зменшені overlap кількість чанків і покриття тексту зменшується, при збільшені overlap кількість чанків і покриття текту збільшується (тобто частини одного і того самого тексту і змісту знаходяться в різних чанках). 

## Частина 5 — Гібридний пошук

| Запит | BM25 | Векторний пошук | Гібридний пошук (RRF) | Висновок |
|-------|------|-----------------|-----------------------|----------|
| **BERT fine-tuning** | Найбільш релевантні статті про BERT, fine-tuning та модифікації переднавчання. Результати точно відповідають ключовим словам запиту. | Переважають сучасні роботи про LLM post-training, reinforcement fine-tuning та diffusion-моделі. Семантична схожість висока, але більшість результатів не стосується безпосередньо BERT. | Поєднує результати BM25 та векторного пошуку, однак у верхніх позиціях залишаються сучасні роботи про fine-tuning без прив'язки до BERT. | **BM25 показав найкращу точність**, гібридний — компромісний варіант, векторний — найбільш семантичний, але менш точний. |
| **Yann LeCun convolutional networks** | Знайдено статті про convolutional neural networks, однак ім'я Yann LeCun практично не вплинуло на результати. | Повертає роботи про сучасні CNN, ConvNeXt, CapsNet та інші архітектури, але без зв'язку з Yann LeCun. | Об'єднує результати обох методів, проте релевантність до автора залишається низькою. | **Жоден метод не знайшов робіт саме про Yann LeCun.** Причиною є відсутність відповідних документів у колекції. |
| **making computers understand human emotions from text** | Знайдено роботи про аналіз емоцій у соціальних мережах та емоційний аналіз тексту. Тематика відповідає запиту. | Семантично близькі роботи про sentiment analysis, emotion recognition, empathetic dialogue та multimodal emotion recognition. | Поєднує роботи про emotion analysis, sentiment analysis та соціальні мережі, забезпечуючи найбільш різноманітну видачу. | **Гібридний пошук показав найкращий баланс** між тематичною релевантністю та різноманітністю результатів. |

1. Метод гібридного пошуку з RRF дав кращий результат тому що гібридний пошук поєднує сильні сторони обох підходів, використовуючи алгоритм Reciprocal Rank Fusion (RRF) для об’єднання точності та семантичного розуміння
2. Є документи в топ-5 гібридного пошуку, яких немає в топ-5 окремих методів. Тому що сукупний скор дозволяє документу 
піднятися в рейтингу топ-5 гібридного пошуку, так як документ може бути присутній в обох рейтигах та займати непогані місця в кожному з них.
3. Зміна параметра k в RRF впливає на видачу (наприклад, k=60 vs k=1) таким чином, що при k=1 в топ рейтинг гібридного пошуку на перші місця попадають документи які займали перщі місця в обох рейтингах.

## Частина 6 — Аналіз і висновки
 1. 