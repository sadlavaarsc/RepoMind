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
| cuezero | llm_only | 0.000 | 0.000 | 0.000 | 0.446 | 0.0% | 50.0% | 0.00 | 2.00 | 1.00 | -2.00 | 21760.5 | 3590 |
| cuezero | naive_rag | 0.500 | 1.000 | 0.260 | 0.627 | 100.0% | 100.0% | 2.00 | 2.00 | 2.00 | 0.00 | 15034.3 | 14100 |
| cuezero | structured_rag | 0.325 | 0.700 | 0.320 | 0.574 | 70.0% | 70.0% | 1.50 | 1.70 | 1.90 | -0.20 | 20691.7 | 4585 |
| cuezero | structured_rag_new_chunk | 0.400 | 0.900 | 0.348 | 0.533 | 70.0% | 70.0% | 1.50 | 1.70 | 2.00 | -0.20 | 18503.5 | 3420 |
| cuezero | full_system | 0.558 | 0.900 | 0.372 | 0.527 | 60.0% | 80.0% | 1.50 | 1.70 | 2.00 | -0.20 | 48915.8 | 2313 |
| cuezero | full_system_fast | 0.558 | 0.900 | 0.337 | 0.469 | 60.0% | 80.0% | 1.50 | 1.80 | 2.00 | -0.30 | 14342.8 | 1634 |
| cuezero | full_system_new_chunk | 0.558 | 0.900 | 0.378 | 0.527 | 70.0% | 80.0% | 1.60 | 1.80 | 2.00 | -0.20 | 42752.6 | 2340 |
| cuezero | full_system_fast_new_chunk | 0.558 | 0.900 | 0.337 | 0.469 | 80.0% | 70.0% | 1.70 | 1.60 | 2.00 | 0.10 | 14732.1 | 1729 |

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
