# RepoMind 基线测试完整指标总结

**测试日期**: 2026-03-24

## travel_agent 项目

| 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 可回答率 | 端到端成功率 | 平均充分性 | 平均正确性 | 平均事实性 | 检索差距 | 平均延迟(ms) | 平均总Token |
|------|-----------|-----------|-----------|------------|---------|------------|---------|---------|---------|--------|------------|-----------|
| llm_only | 0.000 | 0.000 | 0.000 | 0.842 | 0.0% | 40.0% | 0.00 | 2.00 | 0.80 | -2.00 | 14463.6 | 3136 |
| naive_rag | 1.000 | 1.000 | 0.480 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 12789.5 | 3163 |
| structured_rag | 0.950 | 1.000 | 0.583 | 0.930 | 80.0% | 100.0% | 1.70 | 2.00 | 2.00 | -0.30 | 13869.1 | 2998 |
| structured_rag_new_chunk | 0.975 | 1.000 | 0.642 | 0.901 | 80.0% | 100.0% | 1.70 | 2.00 | 2.00 | -0.30 | 15115.2 | 2686 |
| full_system | 0.975 | 1.000 | 0.642 | 0.907 | 40.0% | 50.0% | 0.90 | 2.00 | 1.00 | -1.10 | 37362.6 | 2845 |
| full_system_fast | 0.975 | 1.000 | 0.642 | 0.907 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 15157.2 | 2502 |
| full_system_new_chunk | 0.975 | 1.000 | 0.642 | 0.930 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 38786.0 | 2745 |
| full_system_fast_new_chunk | 0.975 | 1.000 | 0.642 | 0.930 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 13730.5 | 2484 |
| full_system_new_chunk_bilingual | 0.975 | 1.000 | 0.642 | 0.953 | 90.0% | 90.0% | 1.90 | 2.00 | 2.00 | -0.10 | 52035.1 | 2738 |
| full_system_fast_new_chunk_bilingual | 0.975 | 1.000 | 0.642 | 0.930 | 90.0% | 90.0% | 1.90 | 2.00 | 2.00 | -0.10 | 15120.7 | 2527 |
| full_system_fast_new_rerank | 0.875 | 1.000 | 0.475 | 0.918 | 80.0% | 100.0% | 1.80 | 2.00 | 2.00 | -0.20 | 61584.3 | 2742 |
| structured_rag_new_chunk_llm_summary_fixed | 1.000 | 1.000 | 0.585 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 17476.1 | 3416 |
| full_system_new_chunk_llm_summary_fixed | 1.000 | 1.000 | 0.480 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 51349.4 | 4162 |
| full_system_fast_new_chunk_llm_summary_fixed | 1.000 | 1.000 | 0.480 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 12842.7 | 3995 |
| full_system_new_rerank | 0.875 | 1.000 | 0.480 | 0.848 | 80.0% | 100.0% | 1.80 | 2.00 | 2.00 | -0.20 | 100296.6 | 3096 |
| full_system_fast_new_rerank | 0.875 | 1.000 | 0.465 | 0.848 | 80.0% | 100.0% | 1.80 | 2.00 | 2.00 | -0.20 | 58530.0 | 2678 |
| full_system_chinese_rerank_fix | 0.975 | 1.000 | 0.485 | 0.918 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 94292.8 | 3307 |
| full_system_fast_chinese_rerank_fix | 0.975 | 1.000 | 0.490 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 65952.5 | 3170 |

### 详细查询指标

#### llm_only

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.000 | 0.000 | 0.000 | 0.767 | 0.667 | 25193.5 | 2212 | 1615 | 3827 | 4 | 0 | Good - covers most key entities |
| 2 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 5947.3 | 2212 | 379 | 2591 | 4 | 0 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 16118.1 | 2215 | 1088 | 3303 | 1 | 0 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 4124.8 | 2212 | 242 | 2454 | 1 | 0 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 0.000 | 0.000 | 0.000 | 0.650 | 0.500 | 25170.5 | 2216 | 1637 | 3853 | 1 | 0 | Fair - covers some key entities but missing important details |
| 6 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 6696.4 | 2214 | 408 | 2622 | 2 | 0 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 0.000 | 0.000 | 0.000 | 0.767 | 0.667 | 8636.9 | 2213 | 546 | 2759 | 1 | 0 | Good - covers most key entities |
| 8 | 0.000 | 0.000 | 0.000 | 0.475 | 0.250 | 19049.5 | 2217 | 1204 | 3421 | 4 | 0 | Poor - missing most key entities or incomplete answer |
| 9 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 8315.6 | 2219 | 528 | 2747 | 2 | 0 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 0.000 | 0.000 | 0.000 | 0.767 | 0.667 | 25383.9 | 2216 | 1568 | 3784 | 4 | 0 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 14463.6ms
- 总延迟: 144636.5ms
- 平均 Prompt Token: 2215
- 总 Prompt Token: 22146
- 平均 Completion Token: 922
- 总 Completion Token: 9215
- 平均总 Token: 3136
- 总 Token: 31361
- 平均答案质量: 0.842

#### naive_rag

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 22713.7 | 2409 | 1389 | 3798 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 7932.7 | 2409 | 484 | 2893 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 17005.0 | 2412 | 1105 | 3517 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 4180.0 | 2409 | 241 | 2650 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 9663.5 | 2413 | 587 | 3000 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 8272.9 | 2411 | 487 | 2898 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.200 | 0.767 | 0.667 | 11051.4 | 2410 | 577 | 2987 | 1 | 5 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 14673.4 | 2414 | 849 | 3263 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 10116.5 | 2416 | 603 | 3019 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 0.800 | 0.767 | 0.667 | 22285.6 | 2413 | 1195 | 3608 | 4 | 5 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 12789.5ms
- 总延迟: 127894.7ms
- 平均 Prompt Token: 2412
- 总 Prompt Token: 24116
- 平均 Completion Token: 752
- 总 Completion Token: 7517
- 平均总 Token: 3163
- 总 Token: 31633
- 平均答案质量: 0.953

#### structured_rag

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 25928.1 | 2141 | 1667 | 3808 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 18307.2 | 2336 | 1274 | 3610 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 16128.3 | 2339 | 1035 | 3374 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 5689.1 | 2198 | 320 | 2518 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 8704.9 | 2202 | 477 | 2679 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 7881.5 | 1733 | 518 | 2251 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.767 | 0.667 | 9219.1 | 1886 | 528 | 2414 | 1 | 3 | Good - covers most key entities |
| 8 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 15128.6 | 2203 | 878 | 3081 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 8813.7 | 2205 | 539 | 2744 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 0.750 | 1.000 | 0.750 | 0.533 | 0.333 | 22890.7 | 2202 | 1301 | 3503 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 13869.1ms
- 总延迟: 138691.2ms
- 平均 Prompt Token: 2144
- 总 Prompt Token: 21445
- 平均 Completion Token: 854
- 总 Completion Token: 8537
- 平均总 Token: 2998
- 总 Token: 29982
- 平均答案质量: 0.930

#### structured_rag_new_chunk

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 25129.4 | 1683 | 1526 | 3209 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 23223.0 | 2188 | 1465 | 3653 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 16468.1 | 2191 | 1044 | 3235 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 5728.3 | 1665 | 268 | 1933 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.333 | 0.650 | 0.500 | 12158.2 | 1695 | 604 | 2299 | 1 | 3 | Fair - covers some key entities but missing important details |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 8249.4 | 1546 | 508 | 2054 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.767 | 0.667 | 10734.8 | 1745 | 663 | 2408 | 1 | 3 | Good - covers most key entities |
| 8 | 0.750 | 1.000 | 1.000 | 0.825 | 0.750 | 13937.0 | 1696 | 694 | 2390 | 4 | 3 | Good - covers most key entities |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 11059.0 | 2064 | 626 | 2690 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 1.000 | 0.767 | 0.667 | 24464.6 | 1687 | 1297 | 2984 | 4 | 4 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 15115.2ms
- 总延迟: 151151.8ms
- 平均 Prompt Token: 1816
- 总 Prompt Token: 18160
- 平均 Completion Token: 870
- 总 Completion Token: 8695
- 平均总 Token: 2686
- 总 Token: 26855
- 平均答案质量: 0.901

#### full_system

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 61334.0 | 1683 | 1943 | 3626 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 41598.4 | 2188 | 1798 | 3986 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 36363.7 | 2191 | 1064 | 3255 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 20754.2 | 1665 | 345 | 2010 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 50682.0 | 1695 | 540 | 2235 | 1 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 42909.5 | 1546 | 1612 | 3158 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.533 | 0.333 | 23279.1 | 1745 | 568 | 2313 | 1 | 3 | Fair - covers some key entities but missing important details |
| 8 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 35136.9 | 1696 | 730 | 2426 | 4 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 23935.2 | 2064 | 534 | 2598 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 1.000 | 0.533 | 0.333 | 37633.1 | 1687 | 1152 | 2839 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 37362.6ms
- 总延迟: 373626.1ms
- 平均 Prompt Token: 1816
- 总 Prompt Token: 18160
- 平均 Completion Token: 1029
- 总 Completion Token: 10286
- 平均总 Token: 2845
- 总 Token: 28446
- 平均答案质量: 0.907

#### full_system_fast

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 27431.2 | 1683 | 1411 | 3094 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 5367.9 | 2101 | 256 | 2357 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 3414.5 | 2103 | 120 | 2223 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 2616.2 | 1584 | 86 | 1670 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 11997.6 | 1695 | 538 | 2233 | 1 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 27254.5 | 1546 | 1465 | 3011 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.533 | 0.333 | 16686.4 | 1745 | 681 | 2426 | 1 | 3 | Fair - covers some key entities but missing important details |
| 8 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 16846.5 | 1696 | 801 | 2497 | 4 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 12670.0 | 2064 | 604 | 2668 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 1.000 | 0.533 | 0.333 | 27286.8 | 1687 | 1152 | 2839 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 15157.2ms
- 总延迟: 151571.6ms
- 平均 Prompt Token: 1790
- 总 Prompt Token: 17904
- 平均 Completion Token: 711
- 总 Completion Token: 7114
- 平均总 Token: 2502
- 总 Token: 25018
- 平均答案质量: 0.907

#### full_system_new_chunk

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 47967.8 | 1683 | 1579 | 3262 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 37332.5 | 2188 | 1260 | 3448 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 42357.7 | 2191 | 1268 | 3459 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 28934.6 | 1665 | 304 | 1969 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 42150.0 | 1695 | 641 | 2336 | 1 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 43866.0 | 1546 | 1350 | 2896 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.767 | 0.667 | 30300.1 | 1745 | 580 | 2325 | 1 | 3 | Good - covers most key entities |
| 8 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 40452.8 | 1696 | 702 | 2398 | 4 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 32907.1 | 2064 | 516 | 2580 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 1.000 | 0.533 | 0.333 | 41591.2 | 1687 | 1089 | 2776 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 38786.0ms
- 总延迟: 387859.8ms
- 平均 Prompt Token: 1816
- 总 Prompt Token: 18160
- 平均 Completion Token: 929
- 总 Completion Token: 9289
- 平均总 Token: 2745
- 总 Token: 27449
- 平均答案质量: 0.930

#### full_system_fast_new_chunk

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 25334.4 | 1683 | 1361 | 3044 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 5272.2 | 2101 | 249 | 2350 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 2584.6 | 2103 | 99 | 2202 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 2953.6 | 1584 | 91 | 1675 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 10925.1 | 1695 | 499 | 2194 | 1 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 27342.0 | 1546 | 1644 | 3190 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.767 | 0.667 | 12888.7 | 1745 | 580 | 2325 | 1 | 3 | Good - covers most key entities |
| 8 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 15847.1 | 1696 | 787 | 2483 | 4 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 10266.3 | 2064 | 484 | 2548 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 1.000 | 0.533 | 0.333 | 23891.4 | 1687 | 1141 | 2828 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 13730.5ms
- 总延迟: 137305.4ms
- 平均 Prompt Token: 1790
- 总 Prompt Token: 17904
- 平均 Completion Token: 694
- 总 Completion Token: 6935
- 平均总 Token: 2484
- 总 Token: 24839
- 平均答案质量: 0.930

#### full_system_new_chunk_bilingual

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 39830.2 | 1683 | 1558 | 3241 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 35388.7 | 2188 | 1064 | 3252 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 66724.5 | 2191 | 1253 | 3444 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 51591.4 | 1665 | 273 | 1938 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 31168.5 | 1695 | 494 | 2189 | 1 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 69833.5 | 1546 | 1679 | 3225 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 65909.7 | 1745 | 675 | 2420 | 1 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 8 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 78251.9 | 1696 | 760 | 2456 | 4 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 44401.4 | 2064 | 418 | 2482 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 1.000 | 0.533 | 0.333 | 37251.2 | 1687 | 1042 | 2729 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 52035.1ms
- 总延迟: 520351.0ms
- 平均 Prompt Token: 1816
- 总 Prompt Token: 18160
- 平均 Completion Token: 922
- 总 Completion Token: 9216
- 平均总 Token: 2738
- 总 Token: 27376
- 平均答案质量: 0.953

#### full_system_fast_new_chunk_bilingual

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 35458.8 | 1683 | 1928 | 3611 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 7710.9 | 2101 | 250 | 2351 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 3950.0 | 2103 | 120 | 2223 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 3573.0 | 1584 | 90 | 1674 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 12015.1 | 1695 | 550 | 2245 | 1 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 24697.4 | 1546 | 1379 | 2925 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.767 | 0.667 | 14220.5 | 1745 | 711 | 2456 | 1 | 3 | Good - covers most key entities |
| 8 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 14486.2 | 1696 | 692 | 2388 | 4 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 11068.5 | 2064 | 483 | 2547 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 1.000 | 0.533 | 0.333 | 24026.3 | 1687 | 1159 | 2846 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 15120.7ms
- 总延迟: 151206.7ms
- 平均 Prompt Token: 1790
- 总 Prompt Token: 17904
- 平均 Completion Token: 736
- 总 Completion Token: 7362
- 平均总 Token: 2527
- 总 Token: 25266
- 平均答案质量: 0.930

#### full_system_fast_new_rerank

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 78082.1 | 1902 | 1720 | 3622 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 45139.5 | 1876 | 323 | 2199 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 48629.7 | 2499 | 118 | 2617 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 60322.3 | 764 | 93 | 857 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 75503.1 | 1967 | 596 | 2563 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 34763.7 | 2292 | 513 | 2805 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.250 | 0.767 | 0.667 | 62106.0 | 2352 | 565 | 2917 | 1 | 4 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 76727.3 | 2661 | 1254 | 3915 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 0.500 | 1.000 | 0.250 | 0.650 | 0.500 | 56132.9 | 1970 | 441 | 2411 | 2 | 4 | Fair - covers some key entities but missing important details |
| 10 | 0.750 | 1.000 | 0.750 | 0.767 | 0.667 | 78436.2 | 2294 | 1219 | 3513 | 4 | 4 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 61584.3ms
- 总延迟: 615842.8ms
- 平均 Prompt Token: 2058
- 总 Prompt Token: 20577
- 平均 Completion Token: 684
- 总 Completion Token: 6842
- 平均总 Token: 2742
- 总 Token: 27419
- 平均答案质量: 0.918

#### structured_rag_new_chunk_llm_summary_fixed

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 25638.3 | 2604 | 1625 | 4229 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 27165.3 | 2556 | 1847 | 4403 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 31181.9 | 2559 | 1768 | 4327 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 5883.7 | 2050 | 310 | 2360 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 11708.7 | 2362 | 563 | 2925 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 11050.9 | 1996 | 599 | 2595 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 9787.3 | 2305 | 514 | 2819 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 15931.3 | 2609 | 825 | 3434 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 12978.2 | 2563 | 687 | 3250 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 0.800 | 0.533 | 0.333 | 23435.1 | 2608 | 1205 | 3813 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 17476.1ms
- 总延迟: 174760.7ms
- 平均 Prompt Token: 2421
- 总 Prompt Token: 24212
- 平均 Completion Token: 994
- 总 Completion Token: 9943
- 平均总 Token: 3416
- 总 Token: 34155
- 平均答案质量: 0.953

#### full_system_new_chunk_llm_summary_fixed

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 59830.1 | 3463 | 645 | 4108 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 33478.4 | 3463 | 472 | 3935 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 89487.6 | 3466 | 997 | 4463 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 45398.6 | 3463 | 273 | 3736 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 32400.8 | 3467 | 714 | 4181 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 53992.4 | 3465 | 512 | 3977 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.200 | 0.767 | 0.667 | 54243.4 | 3464 | 593 | 4057 | 1 | 5 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 39893.5 | 3468 | 780 | 4248 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 55880.8 | 3470 | 647 | 4117 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 0.800 | 0.767 | 0.667 | 48888.1 | 3467 | 1330 | 4797 | 4 | 5 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 51349.4ms
- 总延迟: 513493.7ms
- 平均 Prompt Token: 3466
- 总 Prompt Token: 34656
- 平均 Completion Token: 696
- 总 Completion Token: 6963
- 平均总 Token: 4162
- 总 Token: 41619
- 平均答案质量: 0.953

#### full_system_fast_new_chunk_llm_summary_fixed

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 15135.2 | 3470 | 686 | 4156 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 5293.7 | 3337 | 211 | 3548 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 4570.3 | 3339 | 134 | 3473 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 3684.9 | 3336 | 90 | 3426 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 15563.7 | 3474 | 709 | 4183 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 11809.4 | 3472 | 487 | 3959 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.200 | 0.767 | 0.667 | 12782.4 | 3471 | 603 | 4074 | 1 | 5 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 21636.5 | 3475 | 974 | 4449 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 14087.6 | 3477 | 652 | 4129 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 0.800 | 0.767 | 0.667 | 23862.8 | 3474 | 1082 | 4556 | 4 | 5 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 12842.7ms
- 总延迟: 128426.5ms
- 平均 Prompt Token: 3432
- 总 Prompt Token: 34325
- 平均 Completion Token: 563
- 总 Completion Token: 5628
- 平均总 Token: 3995
- 总 Token: 39953
- 平均答案质量: 0.953

#### full_system_new_rerank

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 118371.1 | 1921 | 1908 | 3829 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 106719.7 | 1921 | 1273 | 3194 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 86203.2 | 2480 | 937 | 3417 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 103161.3 | 1208 | 1492 | 2700 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.250 | 0.300 | 0.000 | 82510.8 | 1643 | 561 | 2204 | 1 | 4 | Poor - missing most key entities or incomplete answer |
| 6 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 61796.9 | 2315 | 492 | 2807 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.250 | 0.767 | 0.667 | 118291.1 | 2363 | 571 | 2934 | 1 | 4 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 125526.5 | 2683 | 1087 | 3770 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 0.500 | 1.000 | 0.250 | 0.650 | 0.500 | 111501.6 | 1977 | 613 | 2590 | 2 | 4 | Fair - covers some key entities but missing important details |
| 10 | 0.750 | 1.000 | 0.750 | 0.767 | 0.667 | 88884.3 | 2317 | 1195 | 3512 | 4 | 4 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 100296.6ms
- 总延迟: 1002966.5ms
- 平均 Prompt Token: 2083
- 总 Prompt Token: 20828
- 平均 Completion Token: 1013
- 总 Completion Token: 10129
- 平均总 Token: 3096
- 总 Token: 30957
- 平均答案质量: 0.848

#### full_system_fast_new_rerank

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 76366.8 | 1925 | 1505 | 3430 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 41902.0 | 1838 | 191 | 2029 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 52906.6 | 2520 | 99 | 2619 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 0.300 | 0.000 | 41162.7 | 1164 | 55 | 1219 | 1 | 4 | Poor - missing most key entities or incomplete answer |
| 5 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 68381.3 | 1660 | 632 | 2292 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 45365.7 | 2618 | 527 | 3145 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.250 | 0.767 | 0.667 | 46304.0 | 1986 | 632 | 2618 | 1 | 4 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 80744.7 | 2681 | 730 | 3411 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 0.500 | 1.000 | 0.250 | 0.650 | 0.500 | 57474.9 | 1992 | 579 | 2571 | 2 | 4 | Fair - covers some key entities but missing important details |
| 10 | 0.750 | 1.000 | 0.750 | 0.767 | 0.667 | 74691.1 | 2308 | 1133 | 3441 | 4 | 4 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 58530.0ms
- 总延迟: 585299.8ms
- 平均 Prompt Token: 2069
- 总 Prompt Token: 20692
- 平均 Completion Token: 608
- 总 Completion Token: 6083
- 平均总 Token: 2678
- 总 Token: 26775
- 平均答案质量: 0.848

#### full_system_chinese_rerank_fix

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 104475.0 | 1933 | 1538 | 3471 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 93287.1 | 2634 | 513 | 3147 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 0.650 | 0.500 | 104846.6 | 2792 | 284 | 3076 | 1 | 5 | Fair - covers some key entities but missing important details |
| 4 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 72227.2 | 2405 | 304 | 2709 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 115641.1 | 2793 | 669 | 3462 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 78357.7 | 2319 | 437 | 2756 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.200 | 0.767 | 0.667 | 85433.5 | 2790 | 647 | 3437 | 1 | 5 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 102825.4 | 2794 | 952 | 3746 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 85750.3 | 2641 | 617 | 3258 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 0.800 | 0.767 | 0.667 | 100084.5 | 2638 | 1371 | 4009 | 4 | 5 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 94292.8ms
- 总延迟: 942928.4ms
- 平均 Prompt Token: 2574
- 总 Prompt Token: 25739
- 平均 Completion Token: 733
- 总 Completion Token: 7332
- 平均总 Token: 3307
- 总 Token: 33071
- 平均答案质量: 0.918

#### full_system_fast_chinese_rerank_fix

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 58429.4 | 1913 | 1449 | 3362 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 149648.0 | 2518 | 263 | 2781 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 38287.3 | 2670 | 112 | 2782 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 45852.2 | 1874 | 92 | 1966 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 65426.4 | 2778 | 580 | 3358 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 33986.9 | 2304 | 464 | 2768 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.200 | 0.767 | 0.667 | 62766.9 | 2775 | 667 | 3442 | 1 | 5 | Good - covers most key entities |
| 8 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 73203.6 | 2779 | 1419 | 4198 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 59322.9 | 2623 | 600 | 3223 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 1.000 | 1.000 | 0.800 | 0.767 | 0.667 | 72601.2 | 2620 | 1203 | 3823 | 4 | 5 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 65952.5ms
- 总延迟: 659524.8ms
- 平均 Prompt Token: 2485
- 总 Prompt Token: 24854
- 平均 Completion Token: 685
- 总 Completion Token: 6849
- 平均总 Token: 3170
- 总 Token: 31703
- 平均答案质量: 0.953

## cuezero 项目

| 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 可回答率 | 端到端成功率 | 平均充分性 | 平均正确性 | 平均事实性 | 检索差距 | 平均延迟(ms) | 平均总Token |
|------|-----------|-----------|-----------|------------|---------|------------|---------|---------|---------|--------|------------|-----------|
| llm_only | 0.000 | 0.000 | 0.000 | 0.446 | 0.0% | 50.0% | 0.00 | 2.00 | 1.00 | -2.00 | 21760.5 | 3590 |
| naive_rag | 0.500 | 1.000 | 0.260 | 0.627 | 100.0% | 100.0% | 2.00 | 2.00 | 2.00 | 0.00 | 15034.3 | 14100 |
| structured_rag | 0.325 | 0.700 | 0.320 | 0.574 | 70.0% | 70.0% | 1.50 | 1.70 | 1.90 | -0.20 | 20691.7 | 4585 |
| structured_rag_new_chunk | 0.400 | 0.900 | 0.348 | 0.533 | 70.0% | 70.0% | 1.50 | 1.70 | 2.00 | -0.20 | 18503.5 | 3420 |
| full_system | 0.558 | 0.900 | 0.372 | 0.527 | 60.0% | 80.0% | 1.50 | 1.70 | 2.00 | -0.20 | 48915.8 | 2313 |
| full_system_fast | 0.558 | 0.900 | 0.337 | 0.469 | 60.0% | 80.0% | 1.50 | 1.80 | 2.00 | -0.30 | 14342.8 | 1634 |
| full_system_new_chunk | 0.558 | 0.900 | 0.378 | 0.527 | 70.0% | 80.0% | 1.60 | 1.80 | 2.00 | -0.20 | 42752.6 | 2340 |
| full_system_fast_new_chunk | 0.558 | 0.900 | 0.337 | 0.469 | 80.0% | 70.0% | 1.70 | 1.60 | 2.00 | 0.10 | 14732.1 | 1729 |
| full_system_new_chunk_bilingual | 0.508 | 0.900 | 0.358 | 0.557 | 70.0% | 70.0% | 1.70 | 1.80 | 1.90 | -0.10 | 63561.8 | 2872 |
| full_system_fast_new_chunk_bilingual | 0.483 | 0.900 | 0.338 | 0.492 | 60.0% | 60.0% | 1.50 | 1.70 | 2.00 | -0.20 | 15065.8 | 2248 |
| full_system_new_chunk_llm_summary | 0.558 | 1.000 | 0.530 | 0.557 | 60.0% | 40.0% | 1.50 | 1.20 | 1.80 | 0.30 | 77063.3 | 2755 |
| full_system_fast_new_chunk_llm_summary | 0.558 | 1.000 | 0.533 | 0.551 | 60.0% | 40.0% | 1.50 | 1.10 | 1.80 | 0.40 | 18541.7 | 2169 |
| full_system_fast_new_rerank | 0.433 | 1.000 | 0.230 | 0.498 | 80.0% | 60.0% | 1.70 | 1.50 | 2.00 | 0.20 | 207083.7 | 2371 |
| structured_rag_new_chunk_llm_summary_fixed | 0.483 | 0.900 | 0.462 | 0.539 | 60.0% | 40.0% | 1.50 | 1.70 | 1.40 | -0.20 | 26146.8 | 2952 |
| full_system_new_chunk_llm_summary_fixed | 0.650 | 1.000 | 0.383 | 0.644 | 60.0% | 50.0% | 1.50 | 1.80 | 1.50 | -0.30 | 59577.3 | 3945 |
| full_system_fast_new_chunk_llm_summary_fixed | 0.650 | 1.000 | 0.424 | 0.615 | 60.0% | 60.0% | 1.50 | 1.60 | 1.40 | -0.10 | 12379.7 | 3751 |
| full_system_new_rerank | 0.433 | 1.000 | 0.225 | 0.545 | 80.0% | 70.0% | 1.70 | 1.80 | 1.90 | -0.10 | 233201.2 | 3005 |
| full_system_fast_new_rerank | 0.483 | 1.000 | 0.240 | 0.457 | 80.0% | 60.0% | 1.70 | 1.50 | 2.00 | 0.20 | 189829.1 | 2387 |
| full_system_chinese_rerank_fix | 0.450 | 1.000 | 0.225 | 0.504 | 100.0% | 80.0% | 2.00 | 1.90 | 1.90 | 0.10 | 223784.0 | 2777 |
| full_system_fast_chinese_rerank_fix | 0.450 | 1.000 | 0.225 | 0.504 | 100.0% | 90.0% | 2.00 | 1.80 | 2.00 | 0.20 | 183836.5 | 2354 |

### 详细查询指标

#### llm_only

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.000 | 0.000 | 0.000 | 0.533 | 0.333 | 22357.0 | 2263 | 1389 | 3652 | 2 | 0 | Fair - covers some key entities but missing important details |
| 2 | 0.000 | 0.000 | 0.000 | 0.533 | 0.333 | 9972.4 | 2262 | 648 | 2910 | 3 | 0 | Fair - covers some key entities but missing important details |
| 3 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 14461.9 | 2259 | 893 | 3152 | 2 | 0 | Poor - missing most key entities or incomplete answer |
| 4 | 0.000 | 0.000 | 0.000 | 0.650 | 0.500 | 20230.9 | 2263 | 1199 | 3462 | 2 | 0 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 16844.9 | 2263 | 1003 | 3266 | 3 | 0 | Poor - missing most key entities or incomplete answer |
| 6 | 0.000 | 0.000 | 0.000 | 0.475 | 0.250 | 26282.8 | 2263 | 1607 | 3870 | 2 | 0 | Poor - missing most key entities or incomplete answer |
| 7 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 17327.0 | 2262 | 1073 | 3335 | 2 | 0 | Poor - missing most key entities or incomplete answer |
| 8 | 0.000 | 0.000 | 0.000 | 0.533 | 0.333 | 34057.7 | 2269 | 2062 | 4331 | 3 | 0 | Fair - covers some key entities but missing important details |
| 9 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 22854.5 | 2264 | 1350 | 3614 | 4 | 0 | Poor - missing most key entities or incomplete answer |
| 10 | 0.000 | 0.000 | 0.000 | 0.533 | 0.333 | 33215.4 | 2263 | 2048 | 4311 | 4 | 0 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 21760.5ms
- 总延迟: 217604.5ms
- 平均 Prompt Token: 2263
- 总 Prompt Token: 22631
- 平均 Completion Token: 1327
- 总 Completion Token: 13272
- 平均总 Token: 3590
- 总 Token: 35903
- 平均答案质量: 0.446

#### naive_rag

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 25879.2 | 3189 | 1419 | 4608 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 0.400 | 0.533 | 0.333 | 12005.7 | 14298 | 755 | 15053 | 3 | 5 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.200 | 0.825 | 0.750 | 9633.5 | 25080 | 517 | 25597 | 2 | 5 | Good - covers most key entities |
| 4 | 0.500 | 1.000 | 0.200 | 0.650 | 0.500 | 7218.3 | 9612 | 470 | 10082 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.667 | 1.000 | 0.400 | 0.533 | 0.333 | 11485.3 | 13837 | 851 | 14688 | 3 | 5 | Fair - covers some key entities but missing important details |
| 6 | 0.500 | 1.000 | 0.200 | 1.000 | 1.000 | 12748.4 | 12935 | 871 | 13806 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 14340.4 | 26338 | 771 | 27109 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 8 | 0.667 | 1.000 | 0.400 | 0.533 | 0.333 | 17346.2 | 9618 | 1317 | 10935 | 3 | 5 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.200 | 0.825 | 0.750 | 14011.3 | 11542 | 1030 | 12572 | 4 | 5 | Good - covers most key entities |
| 10 | 0.250 | 1.000 | 0.200 | 0.533 | 0.333 | 25674.9 | 5034 | 1517 | 6551 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 15034.3ms
- 总延迟: 150343.2ms
- 平均 Prompt Token: 13148
- 总 Prompt Token: 131483
- 平均 Completion Token: 952
- 总 Completion Token: 9518
- 平均总 Token: 14100
- 总 Token: 141001
- 平均答案质量: 0.627

#### structured_rag

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 10506.5 | 3665 | 544 | 4209 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 1.000 | 0.533 | 0.333 | 43157.0 | 731 | 2521 | 3252 | 3 | 2 | Fair - covers some key entities but missing important details |
| 3 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 10080.3 | 4619 | 537 | 5156 | 2 | 3 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 22829.3 | 2842 | 1405 | 4247 | 2 | 2 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 24174.4 | 1414 | 1473 | 2887 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 43317.1 | 1077 | 2555 | 3632 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 0.500 | 1.000 | 0.333 | 0.533 | 0.333 | 11057.4 | 2708 | 622 | 3330 | 2 | 3 | Fair - covers some key entities but missing important details |
| 8 | 0.333 | 1.000 | 0.500 | 0.533 | 0.333 | 18031.3 | 2582 | 1074 | 3656 | 3 | 2 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.333 | 0.825 | 0.750 | 13015.1 | 1848 | 795 | 2643 | 4 | 3 | Good - covers most key entities |
| 10 | 0.000 | 0.000 | 0.000 | 0.533 | 0.333 | 10748.7 | 11835 | 1005 | 12840 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 20691.7ms
- 总延迟: 206917.1ms
- 平均 Prompt Token: 3332
- 总 Prompt Token: 33321
- 平均 Completion Token: 1253
- 总 Completion Token: 12531
- 平均总 Token: 4585
- 总 Token: 45852
- 平均答案质量: 0.574

#### structured_rag_new_chunk

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 9745.7 | 3665 | 612 | 4277 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 1.000 | 0.533 | 0.333 | 16251.1 | 702 | 1156 | 1858 | 3 | 2 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 10846.4 | 4661 | 604 | 5265 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.333 | 0.650 | 0.500 | 20910.7 | 1185 | 1417 | 2602 | 2 | 3 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 24799.3 | 1165 | 1468 | 2633 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 0.650 | 0.500 | 48662.0 | 1103 | 3117 | 4220 | 2 | 3 | Fair - covers some key entities but missing important details |
| 7 | 0.500 | 1.000 | 0.333 | 0.300 | 0.000 | 10876.6 | 2658 | 676 | 3334 | 2 | 3 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.500 | 0.533 | 0.333 | 15341.1 | 2037 | 883 | 2920 | 3 | 2 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.333 | 0.825 | 0.750 | 9622.1 | 1859 | 591 | 2450 | 4 | 3 | Good - covers most key entities |
| 10 | 0.250 | 1.000 | 0.250 | 0.533 | 0.333 | 17980.4 | 3487 | 1149 | 4636 | 4 | 4 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 18503.5ms
- 总延迟: 185035.4ms
- 平均 Prompt Token: 2252
- 总 Prompt Token: 22522
- 平均 Completion Token: 1167
- 总 Completion Token: 11673
- 平均总 Token: 3420
- 总 Token: 34195
- 平均答案质量: 0.533

#### full_system

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 47644.5 | 461 | 1694 | 2155 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 2 | 1.000 | 1.000 | 0.750 | 0.767 | 0.667 | 34715.3 | 529 | 1099 | 1628 | 3 | 4 | Good - covers most key entities |
| 3 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 33014.7 | 754 | 1000 | 1754 | 2 | 2 | Fair - covers some key entities but missing important details |
| 4 | 1.000 | 1.000 | 0.500 | 0.650 | 0.500 | 33150.9 | 1410 | 1228 | 2638 | 2 | 4 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 42231.0 | 668 | 1661 | 2329 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 105011.9 | 1166 | 1755 | 2921 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 45908.5 | 1790 | 626 | 2416 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.333 | 0.533 | 0.333 | 39802.7 | 2063 | 822 | 2885 | 3 | 3 | Fair - covers some key entities but missing important details |
| 9 | 0.500 | 1.000 | 0.400 | 0.475 | 0.250 | 73238.4 | 717 | 2308 | 3025 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.300 | 0.000 | 34440.4 | 342 | 1037 | 1379 | 4 | 5 | Poor - missing most key entities or incomplete answer |

**性能汇总**:
- 平均延迟: 48915.8ms
- 总延迟: 489158.3ms
- 平均 Prompt Token: 990
- 总 Prompt Token: 9900
- 平均 Completion Token: 1323
- 总 Completion Token: 13230
- 平均总 Token: 2313
- 总 Token: 23130
- 平均答案质量: 0.527

#### full_system_fast

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 6387.3 | 440 | 216 | 656 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 2 | 1.000 | 1.000 | 0.750 | 0.533 | 0.333 | 3347.8 | 511 | 116 | 627 | 3 | 4 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.250 | 0.300 | 0.000 | 3249.2 | 643 | 190 | 833 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 4 | 1.000 | 1.000 | 0.400 | 0.650 | 0.500 | 4573.2 | 820 | 258 | 1078 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 2686.9 | 637 | 100 | 737 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 37981.3 | 1166 | 1904 | 3070 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 15645.8 | 1938 | 686 | 2624 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.333 | 0.533 | 0.333 | 15835.8 | 2063 | 750 | 2813 | 3 | 3 | Fair - covers some key entities but missing important details |
| 9 | 0.500 | 1.000 | 0.400 | 0.475 | 0.250 | 30254.1 | 717 | 1585 | 2302 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.300 | 0.000 | 23466.9 | 342 | 1263 | 1605 | 4 | 5 | Poor - missing most key entities or incomplete answer |

**性能汇总**:
- 平均延迟: 14342.8ms
- 总延迟: 143428.3ms
- 平均 Prompt Token: 928
- 总 Prompt Token: 9277
- 平均 Completion Token: 707
- 总 Completion Token: 7068
- 平均总 Token: 1634
- 总 Token: 16345
- 平均答案质量: 0.469

#### full_system_new_chunk

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 45247.6 | 461 | 1476 | 1937 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 2 | 1.000 | 1.000 | 0.750 | 0.767 | 0.667 | 39416.9 | 529 | 1576 | 2105 | 3 | 4 | Good - covers most key entities |
| 3 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 31932.3 | 754 | 1069 | 1823 | 2 | 2 | Fair - covers some key entities but missing important details |
| 4 | 1.000 | 1.000 | 0.400 | 0.650 | 0.500 | 53128.1 | 854 | 1558 | 2412 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 39657.4 | 668 | 1629 | 2297 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.500 | 1.000 | 1.000 | 39853.3 | 1245 | 1596 | 2841 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 40055.5 | 1790 | 635 | 2425 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.333 | 0.533 | 0.333 | 31980.6 | 2063 | 957 | 3020 | 3 | 3 | Fair - covers some key entities but missing important details |
| 9 | 0.500 | 1.000 | 0.400 | 0.475 | 0.250 | 55623.1 | 717 | 1849 | 2566 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.300 | 0.000 | 50631.0 | 342 | 1634 | 1976 | 4 | 5 | Poor - missing most key entities or incomplete answer |

**性能汇总**:
- 平均延迟: 42752.6ms
- 总延迟: 427525.8ms
- 平均 Prompt Token: 942
- 总 Prompt Token: 9423
- 平均 Completion Token: 1398
- 总 Completion Token: 13979
- 平均总 Token: 2340
- 总 Token: 23402
- 平均答案质量: 0.527

#### full_system_fast_new_chunk

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 4587.4 | 440 | 238 | 678 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 2 | 1.000 | 1.000 | 0.750 | 0.533 | 0.333 | 3082.7 | 511 | 116 | 627 | 3 | 4 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.250 | 0.300 | 0.000 | 1894.1 | 643 | 39 | 682 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 4 | 1.000 | 1.000 | 0.400 | 0.650 | 0.500 | 5715.8 | 820 | 245 | 1065 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 4571.1 | 637 | 100 | 737 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 35684.6 | 1548 | 2058 | 3606 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 13980.8 | 1790 | 718 | 2508 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.333 | 0.533 | 0.333 | 16520.9 | 2063 | 841 | 2904 | 3 | 3 | Fair - covers some key entities but missing important details |
| 9 | 0.500 | 1.000 | 0.400 | 0.475 | 0.250 | 38783.5 | 692 | 2171 | 2863 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.300 | 0.000 | 22500.1 | 342 | 1278 | 1620 | 4 | 5 | Poor - missing most key entities or incomplete answer |

**性能汇总**:
- 平均延迟: 14732.1ms
- 总延迟: 147321.0ms
- 平均 Prompt Token: 949
- 总 Prompt Token: 9486
- 平均 Completion Token: 780
- 总 Completion Token: 7804
- 平均总 Token: 1729
- 总 Token: 17290
- 平均答案质量: 0.469

#### full_system_new_chunk_bilingual

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 58733.9 | 643 | 1707 | 2350 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 1.000 | 1.000 | 0.750 | 0.767 | 0.667 | 73571.2 | 847 | 1269 | 2116 | 3 | 4 | Good - covers most key entities |
| 3 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 51696.7 | 1064 | 1646 | 2710 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 82652.7 | 3198 | 1288 | 4486 | 2 | 2 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 68249.2 | 1099 | 1651 | 2750 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 64566.7 | 1166 | 1491 | 2657 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 70670.5 | 2747 | 692 | 3439 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.500 | 0.533 | 0.333 | 38446.5 | 3122 | 1036 | 4158 | 3 | 2 | Fair - covers some key entities but missing important details |
| 9 | 0.500 | 1.000 | 0.400 | 0.475 | 0.250 | 57464.1 | 765 | 583 | 1348 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.533 | 0.333 | 69566.6 | 953 | 1756 | 2709 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 63561.8ms
- 总延迟: 635618.1ms
- 平均 Prompt Token: 1560
- 总 Prompt Token: 15604
- 平均 Completion Token: 1312
- 总 Completion Token: 13119
- 平均总 Token: 2872
- 总 Token: 28723
- 平均答案质量: 0.557

#### full_system_fast_new_chunk_bilingual

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 7525.5 | 632 | 391 | 1023 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 1.000 | 1.000 | 0.750 | 0.533 | 0.333 | 3850.5 | 617 | 90 | 707 | 3 | 4 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 6606.9 | 745 | 439 | 1184 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 5431.8 | 3040 | 172 | 3212 | 2 | 2 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 5541.7 | 760 | 222 | 982 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 31365.9 | 1166 | 1821 | 2987 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 11215.6 | 2747 | 523 | 3270 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.500 | 0.533 | 0.333 | 19248.0 | 3122 | 974 | 4096 | 3 | 2 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.200 | 0.300 | 0.000 | 26854.8 | 739 | 1473 | 2212 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.300 | 0.000 | 33017.5 | 953 | 1851 | 2804 | 4 | 5 | Poor - missing most key entities or incomplete answer |

**性能汇总**:
- 平均延迟: 15065.8ms
- 总延迟: 150658.2ms
- 平均 Prompt Token: 1452
- 总 Prompt Token: 14521
- 平均 Completion Token: 796
- 总 Completion Token: 7956
- 平均总 Token: 2248
- 总 Token: 22477
- 平均答案质量: 0.492

#### full_system_new_chunk_llm_summary

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.400 | 0.533 | 0.333 | 83490.8 | 834 | 1183 | 2017 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 0.667 | 0.533 | 0.333 | 107200.0 | 867 | 2655 | 3522 | 3 | 3 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.250 | 0.475 | 0.250 | 63029.3 | 687 | 1799 | 2486 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 109789.6 | 2422 | 1545 | 3967 | 2 | 2 | Fair - covers some key entities but missing important details |
| 5 | 0.333 | 1.000 | 0.250 | 0.533 | 0.333 | 65066.5 | 1105 | 1531 | 2636 | 3 | 4 | Fair - covers some key entities but missing important details |
| 6 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 | 112578.5 | 917 | 1308 | 2225 | 2 | 1 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 41983.3 | 2747 | 474 | 3221 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 1.000 | 0.533 | 0.333 | 52378.1 | 2340 | 685 | 3025 | 3 | 1 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.333 | 0.475 | 0.250 | 78265.4 | 619 | 1393 | 2012 | 4 | 3 | Poor - missing most key entities or incomplete answer |
| 10 | 0.500 | 1.000 | 0.400 | 0.533 | 0.333 | 56851.4 | 760 | 1683 | 2443 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 77063.3ms
- 总延迟: 770632.9ms
- 平均 Prompt Token: 1330
- 总 Prompt Token: 13298
- 平均 Completion Token: 1426
- 总 Completion Token: 14256
- 平均总 Token: 2755
- 总 Token: 27554
- 平均答案质量: 0.557

#### full_system_fast_new_chunk_llm_summary

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.400 | 0.533 | 0.333 | 7168.5 | 783 | 361 | 1144 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 0.667 | 0.300 | 0.000 | 6161.5 | 841 | 202 | 1043 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 3 | 0.500 | 1.000 | 0.333 | 0.650 | 0.500 | 12937.6 | 633 | 866 | 1499 | 2 | 3 | Fair - covers some key entities but missing important details |
| 4 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 6079.8 | 2305 | 201 | 2506 | 2 | 2 | Fair - covers some key entities but missing important details |
| 5 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 7002.2 | 980 | 308 | 1288 | 3 | 5 | Fair - covers some key entities but missing important details |
| 6 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 | 48489.6 | 917 | 2176 | 3093 | 2 | 1 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 11663.0 | 2747 | 454 | 3201 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 1.000 | 0.533 | 0.333 | 19292.8 | 2340 | 851 | 3191 | 3 | 1 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.333 | 0.475 | 0.250 | 34781.1 | 579 | 1630 | 2209 | 4 | 3 | Poor - missing most key entities or incomplete answer |
| 10 | 0.500 | 1.000 | 0.400 | 0.533 | 0.333 | 31841.1 | 760 | 1756 | 2516 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 18541.7ms
- 总延迟: 185417.2ms
- 平均 Prompt Token: 1288
- 总 Prompt Token: 12885
- 平均 Completion Token: 880
- 总 Completion Token: 8805
- 平均总 Token: 2169
- 总 Token: 21690
- 平均答案质量: 0.551

#### full_system_fast_new_rerank

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 70962.9 | 711 | 315 | 1026 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 0.400 | 0.533 | 0.333 | 215751.2 | 1385 | 164 | 1549 | 3 | 5 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 247985.4 | 1068 | 82 | 1150 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.200 | 1.000 | 1.000 | 157084.6 | 2688 | 218 | 2906 | 2 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 0.333 | 1.000 | 0.200 | 0.300 | 0.000 | 293198.3 | 1706 | 284 | 1990 | 3 | 5 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.250 | 0.475 | 0.250 | 201197.1 | 1546 | 1791 | 3337 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 7 | 0.500 | 1.000 | 0.250 | 0.300 | 0.000 | 302977.9 | 1875 | 413 | 2288 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 144065.7 | 2181 | 853 | 3034 | 3 | 5 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.200 | 0.475 | 0.250 | 301415.1 | 881 | 2256 | 3137 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.533 | 0.333 | 136198.7 | 1134 | 2159 | 3293 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 207083.7ms
- 总延迟: 2070836.9ms
- 平均 Prompt Token: 1518
- 总 Prompt Token: 15175
- 平均 Completion Token: 854
- 总 Completion Token: 8535
- 平均总 Token: 2371
- 总 Token: 23710
- 平均答案质量: 0.498

#### structured_rag_new_chunk_llm_summary_fixed

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 0.533 | 0.333 | 23460.4 | 1434 | 1297 | 2731 | 2 | 2 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 0.667 | 0.533 | 0.333 | 33114.3 | 932 | 1929 | 2861 | 3 | 3 | Fair - covers some key entities but missing important details |
| 3 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 17936.5 | 1448 | 1065 | 2513 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.200 | 0.650 | 0.500 | 20381.9 | 1147 | 1188 | 2335 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.333 | 1.000 | 0.250 | 0.533 | 0.333 | 35527.7 | 1380 | 2181 | 3561 | 3 | 4 | Fair - covers some key entities but missing important details |
| 6 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 | 26371.5 | 1334 | 1671 | 3005 | 2 | 1 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 9772.5 | 3293 | 502 | 3795 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.333 | 0.533 | 0.333 | 37765.2 | 1299 | 2127 | 3426 | 3 | 3 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.333 | 0.475 | 0.250 | 29078.7 | 864 | 1646 | 2510 | 4 | 3 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.333 | 0.533 | 0.333 | 28058.8 | 1053 | 1728 | 2781 | 4 | 3 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 26146.8ms
- 总延迟: 261467.5ms
- 平均 Prompt Token: 1418
- 总 Prompt Token: 14184
- 平均 Completion Token: 1533
- 总 Completion Token: 15334
- 平均总 Token: 2952
- 总 Token: 29518
- 平均答案质量: 0.539

#### full_system_new_chunk_llm_summary_fixed

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.200 | 0.533 | 0.333 | 44178.8 | 2275 | 601 | 2876 | 2 | 10 | Fair - covers some key entities but missing important details |
| 2 | 1.000 | 1.000 | 0.500 | 0.533 | 0.333 | 62310.1 | 2509 | 1409 | 3918 | 3 | 6 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.143 | 1.000 | 1.000 | 80233.9 | 2491 | 1046 | 3537 | 2 | 7 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 0.500 | 1.000 | 0.500 | 1.000 | 1.000 | 98292.1 | 4966 | 515 | 5481 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 0.667 | 1.000 | 0.333 | 0.300 | 0.000 | 43857.0 | 2650 | 595 | 3245 | 3 | 6 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.500 | 1.000 | 1.000 | 45049.8 | 2487 | 765 | 3252 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.500 | 0.300 | 0.000 | 35531.7 | 4724 | 680 | 5404 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.500 | 0.533 | 0.333 | 75627.6 | 4983 | 883 | 5866 | 3 | 2 | Fair - covers some key entities but missing important details |
| 9 | 0.500 | 1.000 | 0.400 | 0.475 | 0.250 | 48625.8 | 1721 | 886 | 2607 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.500 | 1.000 | 0.250 | 0.767 | 0.667 | 62066.0 | 2201 | 1067 | 3268 | 4 | 8 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 59577.3ms
- 总延迟: 595772.8ms
- 平均 Prompt Token: 3101
- 总 Prompt Token: 31007
- 平均 Completion Token: 845
- 总 Completion Token: 8447
- 平均总 Token: 3945
- 总 Token: 39454
- 平均答案质量: 0.644

#### full_system_fast_new_chunk_llm_summary_fixed

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.200 | 0.533 | 0.333 | 6620.4 | 2167 | 428 | 2595 | 2 | 10 | Fair - covers some key entities but missing important details |
| 2 | 1.000 | 1.000 | 0.600 | 0.767 | 0.667 | 5733.2 | 2320 | 185 | 2505 | 3 | 5 | Good - covers most key entities |
| 3 | 0.500 | 1.000 | 0.250 | 0.475 | 0.250 | 10926.0 | 2076 | 749 | 2825 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.500 | 1.000 | 1.000 | 5754.6 | 4825 | 240 | 5065 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 0.667 | 1.000 | 0.333 | 0.300 | 0.000 | 10630.4 | 2309 | 436 | 2745 | 3 | 6 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 15901.0 | 2884 | 734 | 3618 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.400 | 0.300 | 0.000 | 11797.3 | 5189 | 548 | 5737 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 1.000 | 0.533 | 0.333 | 22351.2 | 5665 | 1174 | 6839 | 3 | 1 | Fair - covers some key entities but missing important details |
| 9 | 0.500 | 1.000 | 0.333 | 0.475 | 0.250 | 14075.8 | 1784 | 654 | 2438 | 4 | 6 | Poor - missing most key entities or incomplete answer |
| 10 | 0.500 | 1.000 | 0.286 | 0.767 | 0.667 | 20007.0 | 2106 | 1036 | 3142 | 4 | 7 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 12379.7ms
- 总延迟: 123796.9ms
- 平均 Prompt Token: 3132
- 总 Prompt Token: 31325
- 平均 Completion Token: 618
- 总 Completion Token: 6184
- 平均总 Token: 3751
- 总 Token: 37509
- 平均答案质量: 0.615

#### full_system_new_rerank

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 129263.8 | 727 | 1706 | 2433 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 0.400 | 0.767 | 0.667 | 251163.5 | 1657 | 1153 | 2810 | 3 | 5 | Good - covers most key entities |
| 3 | 0.500 | 1.000 | 0.200 | 0.650 | 0.500 | 290983.9 | 1310 | 2009 | 3319 | 2 | 5 | Fair - covers some key entities but missing important details |
| 4 | 0.500 | 1.000 | 0.200 | 0.650 | 0.500 | 171215.7 | 2756 | 1303 | 4059 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 335285.5 | 1532 | 2010 | 3542 | 3 | 5 | Fair - covers some key entities but missing important details |
| 6 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 230219.1 | 1742 | 1635 | 3377 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 7 | 0.500 | 1.000 | 0.250 | 0.300 | 0.000 | 290857.6 | 1849 | 455 | 2304 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 184281.9 | 2376 | 964 | 3340 | 3 | 5 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.200 | 0.475 | 0.250 | 275754.0 | 1022 | 574 | 1596 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.533 | 0.333 | 172986.9 | 891 | 2381 | 3272 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 233201.2ms
- 总延迟: 2332011.9ms
- 平均 Prompt Token: 1586
- 总 Prompt Token: 15862
- 平均 Completion Token: 1419
- 总 Completion Token: 14190
- 平均总 Token: 3005
- 总 Token: 30052
- 平均答案质量: 0.545

#### full_system_fast_new_rerank

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.200 | 0.533 | 0.333 | 70497.5 | 704 | 384 | 1088 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 0.400 | 0.300 | 0.000 | 200292.4 | 1341 | 189 | 1530 | 3 | 5 | Poor - missing most key entities or incomplete answer |
| 3 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 285096.2 | 900 | 544 | 1444 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.200 | 0.650 | 0.500 | 127067.1 | 2672 | 268 | 2940 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.333 | 1.000 | 0.200 | 0.300 | 0.000 | 275376.3 | 1532 | 165 | 1697 | 3 | 5 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 185960.0 | 1758 | 2224 | 3982 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 7 | 1.000 | 1.000 | 0.400 | 0.300 | 0.000 | 236847.0 | 2596 | 541 | 3137 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 129044.6 | 2138 | 866 | 3004 | 3 | 5 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.200 | 0.475 | 0.250 | 253082.3 | 1031 | 500 | 1531 | 4 | 5 | Poor - missing most key entities or incomplete answer |
| 10 | 0.250 | 1.000 | 0.200 | 0.533 | 0.333 | 135027.5 | 1363 | 2154 | 3517 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 189829.1ms
- 总延迟: 1898290.9ms
- 平均 Prompt Token: 1604
- 总 Prompt Token: 16035
- 平均 Completion Token: 784
- 总 Completion Token: 7835
- 平均总 Token: 2387
- 总 Token: 23870
- 平均答案质量: 0.457

#### full_system_chinese_rerank_fix

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.400 | 0.533 | 0.333 | 123481.3 | 906 | 1419 | 2325 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 312132.8 | 2494 | 1207 | 3701 | 3 | 5 | Fair - covers some key entities but missing important details |
| 3 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 333066.4 | 1029 | 1457 | 2486 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.200 | 0.650 | 0.500 | 159051.1 | 2774 | 1242 | 4016 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 256133.7 | 1485 | 1586 | 3071 | 3 | 5 | Fair - covers some key entities but missing important details |
| 6 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 185810.3 | 1323 | 741 | 2064 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 7 | 0.500 | 1.000 | 0.250 | 0.300 | 0.000 | 336437.7 | 1948 | 434 | 2382 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 167180.8 | 2377 | 895 | 3272 | 3 | 5 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.200 | 0.650 | 0.500 | 230359.9 | 1455 | 731 | 2186 | 4 | 5 | Fair - covers some key entities but missing important details |
| 10 | 0.250 | 1.000 | 0.200 | 0.533 | 0.333 | 134186.2 | 1410 | 854 | 2264 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 223784.0ms
- 总延迟: 2237840.2ms
- 平均 Prompt Token: 1720
- 总 Prompt Token: 17201
- 平均 Completion Token: 1057
- 总 Completion Token: 10566
- 平均总 Token: 2777
- 总 Token: 27767
- 平均答案质量: 0.504

#### full_system_fast_chinese_rerank_fix

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 0.400 | 0.533 | 0.333 | 74175.0 | 884 | 330 | 1214 | 2 | 5 | Fair - covers some key entities but missing important details |
| 2 | 0.333 | 1.000 | 0.200 | 0.767 | 0.667 | 175817.1 | 1485 | 162 | 1647 | 3 | 5 | Good - covers most key entities |
| 3 | 0.500 | 1.000 | 0.200 | 0.300 | 0.000 | 209388.3 | 1191 | 38 | 1229 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.200 | 0.650 | 0.500 | 138442.0 | 2725 | 199 | 2924 | 2 | 5 | Fair - covers some key entities but missing important details |
| 5 | 0.333 | 1.000 | 0.200 | 0.300 | 0.000 | 246362.6 | 1428 | 355 | 1783 | 3 | 5 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.200 | 0.475 | 0.250 | 188993.2 | 1337 | 2292 | 3629 | 2 | 5 | Poor - missing most key entities or incomplete answer |
| 7 | 0.500 | 1.000 | 0.250 | 0.300 | 0.000 | 326985.4 | 1955 | 465 | 2420 | 2 | 4 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.200 | 0.533 | 0.333 | 136070.2 | 2385 | 727 | 3112 | 3 | 5 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.200 | 0.650 | 0.500 | 203703.4 | 1454 | 590 | 2044 | 4 | 5 | Fair - covers some key entities but missing important details |
| 10 | 0.250 | 1.000 | 0.200 | 0.533 | 0.333 | 138428.1 | 1364 | 2177 | 3541 | 4 | 5 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 183836.5ms
- 总延迟: 1838365.3ms
- 平均 Prompt Token: 1621
- 总 Prompt Token: 16208
- 平均 Completion Token: 734
- 总 Completion Token: 7335
- 平均总 Token: 2354
- 总 Token: 23543
- 平均答案质量: 0.504

## 总体对比

| 项目 | 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 可回答率 | 端到端成功率 | 平均充分性 | 平均正确性 | 平均事实性 | 检索差距 | 平均延迟(ms) | 平均总Token |
|------|------|-----------|-----------|-----------|------------|---------|------------|---------|---------|---------|--------|------------|-----------|
| travel_agent | llm_only | 0.000 | 0.000 | 0.000 | 0.842 | 0.0% | 40.0% | 0.00 | 2.00 | 0.80 | -2.00 | 14463.6 | 3136 |
| travel_agent | naive_rag | 1.000 | 1.000 | 0.480 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 12789.5 | 3163 |
| travel_agent | structured_rag | 0.950 | 1.000 | 0.583 | 0.930 | 80.0% | 100.0% | 1.70 | 2.00 | 2.00 | -0.30 | 13869.1 | 2998 |
| travel_agent | structured_rag_new_chunk | 0.975 | 1.000 | 0.642 | 0.901 | 80.0% | 100.0% | 1.70 | 2.00 | 2.00 | -0.30 | 15115.2 | 2686 |
| travel_agent | full_system | 0.975 | 1.000 | 0.642 | 0.907 | 40.0% | 50.0% | 0.90 | 2.00 | 1.00 | -1.10 | 37362.6 | 2845 |
| travel_agent | full_system_fast | 0.975 | 1.000 | 0.642 | 0.907 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 15157.2 | 2502 |
| travel_agent | full_system_new_chunk | 0.975 | 1.000 | 0.642 | 0.930 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 38786.0 | 2745 |
| travel_agent | full_system_fast_new_chunk | 0.975 | 1.000 | 0.642 | 0.930 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 13730.5 | 2484 |
| travel_agent | full_system_new_chunk_bilingual | 0.975 | 1.000 | 0.642 | 0.953 | 90.0% | 90.0% | 1.90 | 2.00 | 2.00 | -0.10 | 52035.1 | 2738 |
| travel_agent | full_system_fast_new_chunk_bilingual | 0.975 | 1.000 | 0.642 | 0.930 | 90.0% | 90.0% | 1.90 | 2.00 | 2.00 | -0.10 | 15120.7 | 2527 |
| travel_agent | full_system_fast_new_rerank | 0.875 | 1.000 | 0.475 | 0.918 | 80.0% | 100.0% | 1.80 | 2.00 | 2.00 | -0.20 | 61584.3 | 2742 |
| cuezero | llm_only | 0.000 | 0.000 | 0.000 | 0.446 | 0.0% | 50.0% | 0.00 | 2.00 | 1.00 | -2.00 | 21760.5 | 3590 |
| cuezero | naive_rag | 0.500 | 1.000 | 0.260 | 0.627 | 100.0% | 100.0% | 2.00 | 2.00 | 2.00 | 0.00 | 15034.3 | 14100 |
| cuezero | structured_rag | 0.325 | 0.700 | 0.320 | 0.574 | 70.0% | 70.0% | 1.50 | 1.70 | 1.90 | -0.20 | 20691.7 | 4585 |
| cuezero | structured_rag_new_chunk | 0.400 | 0.900 | 0.348 | 0.533 | 70.0% | 70.0% | 1.50 | 1.70 | 2.00 | -0.20 | 18503.5 | 3420 |
| cuezero | full_system | 0.558 | 0.900 | 0.372 | 0.527 | 60.0% | 80.0% | 1.50 | 1.70 | 2.00 | -0.20 | 48915.8 | 2313 |
| cuezero | full_system_fast | 0.558 | 0.900 | 0.337 | 0.469 | 60.0% | 80.0% | 1.50 | 1.80 | 2.00 | -0.30 | 14342.8 | 1634 |
| cuezero | full_system_new_chunk | 0.558 | 0.900 | 0.378 | 0.527 | 70.0% | 80.0% | 1.60 | 1.80 | 2.00 | -0.20 | 42752.6 | 2340 |
| cuezero | full_system_fast_new_chunk | 0.558 | 0.900 | 0.337 | 0.469 | 80.0% | 70.0% | 1.70 | 1.60 | 2.00 | 0.10 | 14732.1 | 1729 |
| cuezero | full_system_new_chunk_bilingual | 0.508 | 0.900 | 0.358 | 0.557 | 70.0% | 70.0% | 1.70 | 1.80 | 1.90 | -0.10 | 63561.8 | 2872 |
| cuezero | full_system_fast_new_chunk_bilingual | 0.483 | 0.900 | 0.338 | 0.492 | 60.0% | 60.0% | 1.50 | 1.70 | 2.00 | -0.20 | 15065.8 | 2248 |
| cuezero | full_system_new_chunk_llm_summary | 0.558 | 1.000 | 0.530 | 0.557 | 60.0% | 40.0% | 1.50 | 1.20 | 1.80 | 0.30 | 77063.3 | 2755 |
| cuezero | full_system_fast_new_chunk_llm_summary | 0.558 | 1.000 | 0.533 | 0.551 | 60.0% | 40.0% | 1.50 | 1.10 | 1.80 | 0.40 | 18541.7 | 2169 |
| cuezero | full_system_fast_new_rerank | 0.433 | 1.000 | 0.230 | 0.498 | 80.0% | 60.0% | 1.70 | 1.50 | 2.00 | 0.20 | 207083.7 | 2371 |
| travel_agent | structured_rag_new_chunk_llm_summary_fixed | 1.000 | 1.000 | 0.585 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 17476.1 | 3416 |
| travel_agent | full_system_new_chunk_llm_summary_fixed | 1.000 | 1.000 | 0.480 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 51349.4 | 4162 |
| travel_agent | full_system_fast_new_chunk_llm_summary_fixed | 1.000 | 1.000 | 0.480 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 12842.7 | 3995 |
| cuezero | structured_rag_new_chunk_llm_summary_fixed | 0.483 | 0.900 | 0.462 | 0.539 | 60.0% | 40.0% | 1.50 | 1.70 | 1.40 | -0.20 | 26146.8 | 2952 |
| cuezero | full_system_new_chunk_llm_summary_fixed | 0.650 | 1.000 | 0.383 | 0.644 | 60.0% | 50.0% | 1.50 | 1.80 | 1.50 | -0.30 | 59577.3 | 3945 |
| cuezero | full_system_fast_new_chunk_llm_summary_fixed | 0.650 | 1.000 | 0.424 | 0.615 | 60.0% | 60.0% | 1.50 | 1.60 | 1.40 | -0.10 | 12379.7 | 3751 |
| travel_agent | full_system_new_rerank | 0.875 | 1.000 | 0.480 | 0.848 | 80.0% | 100.0% | 1.80 | 2.00 | 2.00 | -0.20 | 100296.6 | 3096 |
| travel_agent | full_system_fast_new_rerank | 0.875 | 1.000 | 0.465 | 0.848 | 80.0% | 100.0% | 1.80 | 2.00 | 2.00 | -0.20 | 58530.0 | 2678 |
| cuezero | full_system_new_rerank | 0.433 | 1.000 | 0.225 | 0.545 | 80.0% | 70.0% | 1.70 | 1.80 | 1.90 | -0.10 | 233201.2 | 3005 |
| cuezero | full_system_fast_new_rerank | 0.483 | 1.000 | 0.240 | 0.457 | 80.0% | 60.0% | 1.70 | 1.50 | 2.00 | 0.20 | 189829.1 | 2387 |
| travel_agent | full_system_chinese_rerank_fix | 0.975 | 1.000 | 0.485 | 0.918 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 94292.8 | 3307 |
| travel_agent | full_system_fast_chinese_rerank_fix | 0.975 | 1.000 | 0.490 | 0.953 | 90.0% | 100.0% | 1.90 | 2.00 | 2.00 | -0.10 | 65952.5 | 3170 |
| cuezero | full_system_chinese_rerank_fix | 0.450 | 1.000 | 0.225 | 0.504 | 100.0% | 80.0% | 2.00 | 1.90 | 1.90 | 0.10 | 223784.0 | 2777 |
| cuezero | full_system_fast_chinese_rerank_fix | 0.450 | 1.000 | 0.225 | 0.504 | 100.0% | 90.0% | 2.00 | 1.80 | 2.00 | 0.20 | 183836.5 | 2354 |

## 指标说明

### 检索指标
- **召回率 (Recall)**: 检索到的相关文件数 / 总相关文件数
- **命中率 (Hit Rate)**: 是否至少检索到一个相关文件 (1.0 或 0.0)
- **精确率 (Precision)**: 检索到的相关文件数 / 总检索文件数
- **答案质量 (Quality Score)**: 基于关键实体覆盖率和答案完整性的综合评分 (0.0-1.0)
- **实体覆盖率 (Entity Coverage)**: 答案中包含的期望关键实体比例

### LLM 评估指标
- **可回答率 (Answerable Rate)**: 检索上下文被判定为完全充分的查询比例 (sufficiency == 2)
- **端到端成功率 (End-to-end Success Rate)**: 答案既正确又完全基于上下文的查询比例 (correctness == 2 AND grounding == 2)
- **平均充分性 (Avg Sufficiency)**: 检索上下文充分性的平均分 (0-2)
- **平均正确性 (Avg Correctness)**: 答案正确性的平均分 (0-2)
- **平均事实性 (Avg Grounding)**: 答案事实性的平均分 (0-2)
- **检索差距 (Retrieval Gap)**: avg(sufficiency - correctness)，正值表示检索弱，负值表示生成弱

### 性能指标
- **延迟 (Latency)**: 每个查询的平均响应时间 (毫秒)
- **Token 使用**: Prompt + Completion 的总 Token 数
