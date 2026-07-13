# Zazhytskyi_nosql_2

## Частина 1 — Підготовка даних і вибір інструментів

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
