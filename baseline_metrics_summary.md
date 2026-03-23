# RepoMind 基线测试完整指标总结

**测试日期**: 2026-03-23

## travel_agent 项目

| 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 平均延迟(ms) | 平均总Token |
|------|-----------|-----------|-----------|------------|------------|-----------|
| llm_only | 0.000 | 0.000 | 0.000 | 0.842 | 14463.6 | 3136 |
| naive_rag | 1.000 | 1.000 | 0.480 | 0.953 | 12789.5 | 3163 |
| structured_rag | 0.950 | 1.000 | 0.583 | 0.930 | 13869.1 | 2998 |
| full_system | 0.950 | 1.000 | 0.583 | 0.918 | 36984.0 | 3123 |
| full_system_fast | 0.950 | 1.000 | 0.583 | 0.907 | 14474.7 | 2919 |

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

#### full_system

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 34908.2 | 2141 | 1295 | 3436 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 43878.8 | 2336 | 1523 | 3859 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 34653.0 | 2339 | 1195 | 3534 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 18405.9 | 2198 | 351 | 2549 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.250 | 0.650 | 0.500 | 29288.8 | 2202 | 559 | 2761 | 1 | 4 | Fair - covers some key entities but missing important details |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 37895.5 | 1733 | 1275 | 3008 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.767 | 0.667 | 30651.5 | 1886 | 573 | 2459 | 1 | 3 | Good - covers most key entities |
| 8 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 35827.8 | 2203 | 1004 | 3207 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 32781.2 | 2205 | 618 | 2823 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 0.750 | 1.000 | 0.750 | 0.767 | 0.667 | 71548.9 | 2202 | 1390 | 3592 | 4 | 4 | Good - covers most key entities |

**性能汇总**:
- 平均延迟: 36984.0ms
- 总延迟: 369839.6ms
- 平均 Prompt Token: 2144
- 总 Prompt Token: 21445
- 平均 Completion Token: 978
- 总 Completion Token: 9783
- 平均总 Token: 3123
- 总 Token: 31228
- 平均答案质量: 0.918

#### full_system_fast

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 32079.0 | 2141 | 1918 | 4059 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 2 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 5887.1 | 2239 | 250 | 2489 | 4 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 3 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 3360.5 | 2241 | 97 | 2338 | 1 | 5 | Excellent - covers all key entities and provides detailed explanation |
| 4 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 3069.7 | 2098 | 93 | 2191 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 1.000 | 1.000 | 0.250 | 1.000 | 1.000 | 13179.8 | 2202 | 729 | 2931 | 1 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 28399.8 | 1733 | 1930 | 3663 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 1.000 | 1.000 | 0.333 | 0.767 | 0.667 | 11407.6 | 1886 | 609 | 2495 | 1 | 3 | Good - covers most key entities |
| 8 | 0.750 | 1.000 | 0.750 | 1.000 | 1.000 | 16415.2 | 2203 | 861 | 3064 | 4 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 9 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 10672.3 | 2205 | 520 | 2725 | 2 | 4 | Excellent - covers all key entities and provides detailed explanation |
| 10 | 0.750 | 1.000 | 0.750 | 0.300 | 0.000 | 20275.8 | 2202 | 1032 | 3234 | 4 | 4 | Poor - missing most key entities or incomplete answer |

**性能汇总**:
- 平均延迟: 14474.7ms
- 总延迟: 144746.8ms
- 平均 Prompt Token: 2115
- 总 Prompt Token: 21150
- 平均 Completion Token: 804
- 总 Completion Token: 8039
- 平均总 Token: 2919
- 总 Token: 29189
- 平均答案质量: 0.907

## cuezero 项目

| 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 平均延迟(ms) | 平均总Token |
|------|-----------|-----------|-----------|------------|------------|-----------|
| llm_only | 0.000 | 0.000 | 0.000 | 0.446 | 21760.5 | 3590 |
| naive_rag | 0.500 | 1.000 | 0.260 | 0.627 | 15034.3 | 14100 |
| structured_rag | 0.000 | 0.000 | 0.000 | 0.167 | 9038.7 | 2218 |
| full_system | 0.400 | 0.900 | 0.475 | 0.609 | 82998.6 | 3499 |
| full_system_fast | 0.400 | 0.900 | 0.408 | 0.603 | 11706.0 | 2729 |

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
| 1 | 0.000 | 0.000 | 0.000 | 0.533 | 0.333 | 28454.2 | 1465 | 1761 | 3226 | 2 | 2 | Fair - covers some key entities but missing important details |
| 2 | 0.000 | 0.000 | 0.000 | 0.533 | 0.333 | 12063.5 | 12020 | 687 | 12707 | 3 | 2 | Fair - covers some key entities but missing important details |
| 3 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 24472.2 | 1400 | 1612 | 3012 | 2 | 2 | Poor - missing most key entities or incomplete answer |
| 4 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 25397.2 | 1594 | 1639 | 3233 | 2 | 2 | Poor - missing most key entities or incomplete answer |
| 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0 | 0 | 0 | 3 | 0 | No answer provided |
| 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0 | 0 | 0 | 2 | 0 | No answer provided |
| 7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0 | 0 | 0 | 2 | 0 | No answer provided |
| 8 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0 | 0 | 0 | 3 | 0 | No answer provided |
| 9 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0 | 0 | 0 | 4 | 0 | No answer provided |
| 10 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0 | 0 | 0 | 4 | 0 | No answer provided |

**性能汇总**:
- 平均延迟: 9038.7ms
- 总延迟: 90387.1ms
- 平均 Prompt Token: 1648
- 总 Prompt Token: 16479
- 平均 Completion Token: 570
- 总 Completion Token: 5699
- 平均总 Token: 2218
- 总 Token: 22178
- 平均答案质量: 0.167

#### full_system

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.250 | 0.533 | 0.333 | 26819.5 | 3563 | 651 | 4214 | 2 | 4 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 1.000 | 0.767 | 0.667 | 150665.0 | 731 | 3424 | 4155 | 3 | 2 | Good - covers most key entities |
| 3 | 0.500 | 1.000 | 1.000 | 0.650 | 0.500 | 36310.0 | 641 | 1205 | 1846 | 2 | 1 | Fair - covers some key entities but missing important details |
| 4 | 0.500 | 1.000 | 0.500 | 0.650 | 0.500 | 53566.0 | 3174 | 2065 | 5239 | 2 | 2 | Fair - covers some key entities but missing important details |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 40011.7 | 1414 | 1488 | 2902 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 46910.5 | 1274 | 1962 | 3236 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 0.500 | 1.000 | 0.500 | 0.300 | 0.000 | 25819.7 | 1855 | 525 | 2380 | 2 | 2 | Poor - missing most key entities or incomplete answer |
| 8 | 0.333 | 1.000 | 0.500 | 0.533 | 0.333 | 364228.3 | 3180 | 844 | 4024 | 3 | 2 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.333 | 0.825 | 0.750 | 53638.6 | 1776 | 796 | 2572 | 4 | 3 | Good - covers most key entities |
| 10 | 0.250 | 1.000 | 0.333 | 0.533 | 0.333 | 32016.7 | 3562 | 861 | 4423 | 4 | 3 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 82998.6ms
- 总延迟: 829986.0ms
- 平均 Prompt Token: 2117
- 总 Prompt Token: 21170
- 平均 Completion Token: 1382
- 总 Completion Token: 13821
- 平均总 Token: 3499
- 总 Token: 34991
- 平均答案质量: 0.609

#### full_system_fast

| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |
|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|
| 1 | 0.500 | 1.000 | 0.250 | 0.533 | 0.333 | 8374.8 | 3556 | 447 | 4003 | 2 | 4 | Fair - covers some key entities but missing important details |
| 2 | 0.667 | 1.000 | 1.000 | 0.300 | 0.000 | 3817.0 | 677 | 161 | 838 | 3 | 2 | Poor - missing most key entities or incomplete answer |
| 3 | 0.500 | 1.000 | 0.333 | 0.475 | 0.250 | 4219.6 | 463 | 241 | 704 | 2 | 3 | Poor - missing most key entities or incomplete answer |
| 4 | 0.500 | 1.000 | 0.500 | 1.000 | 1.000 | 4176.5 | 3019 | 172 | 3191 | 2 | 2 | Excellent - covers all key entities and provides detailed explanation |
| 5 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 4637.2 | 1325 | 257 | 1582 | 3 | 3 | Poor - missing most key entities or incomplete answer |
| 6 | 0.500 | 1.000 | 0.333 | 1.000 | 1.000 | 29358.5 | 1274 | 1806 | 3080 | 2 | 3 | Excellent - covers all key entities and provides detailed explanation |
| 7 | 0.500 | 1.000 | 0.500 | 0.533 | 0.333 | 11055.7 | 1855 | 626 | 2481 | 2 | 2 | Fair - covers some key entities but missing important details |
| 8 | 0.333 | 1.000 | 0.500 | 0.533 | 0.333 | 19252.2 | 3180 | 968 | 4148 | 3 | 2 | Fair - covers some key entities but missing important details |
| 9 | 0.250 | 1.000 | 0.333 | 0.825 | 0.750 | 14829.8 | 1848 | 847 | 2695 | 4 | 3 | Good - covers most key entities |
| 10 | 0.250 | 1.000 | 0.333 | 0.533 | 0.333 | 17339.2 | 3562 | 1010 | 4572 | 4 | 3 | Fair - covers some key entities but missing important details |

**性能汇总**:
- 平均延迟: 11706.0ms
- 总延迟: 117060.5ms
- 平均 Prompt Token: 2076
- 总 Prompt Token: 20759
- 平均 Completion Token: 654
- 总 Completion Token: 6535
- 平均总 Token: 2729
- 总 Token: 27294
- 平均答案质量: 0.603

## 总体对比

| 项目 | 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 平均延迟(ms) | 平均总Token |
|------|------|-----------|-----------|-----------|------------|------------|-----------|
| travel_agent | llm_only | 0.000 | 0.000 | 0.000 | 0.842 | 14463.6 | 3136 |
| travel_agent | naive_rag | 1.000 | 1.000 | 0.480 | 0.953 | 12789.5 | 3163 |
| travel_agent | structured_rag | 0.950 | 1.000 | 0.583 | 0.930 | 13869.1 | 2998 |
| travel_agent | full_system | 0.950 | 1.000 | 0.583 | 0.918 | 36984.0 | 3123 |
| travel_agent | full_system_fast | 0.950 | 1.000 | 0.583 | 0.907 | 14474.7 | 2919 |
| cuezero | llm_only | 0.000 | 0.000 | 0.000 | 0.446 | 21760.5 | 3590 |
| cuezero | naive_rag | 0.500 | 1.000 | 0.260 | 0.627 | 15034.3 | 14100 |
| cuezero | structured_rag | 0.000 | 0.000 | 0.000 | 0.167 | 9038.7 | 2218 |
| cuezero | full_system | 0.400 | 0.900 | 0.475 | 0.609 | 82998.6 | 3499 |
| cuezero | full_system_fast | 0.400 | 0.900 | 0.408 | 0.603 | 11706.0 | 2729 |

## 指标说明

- **召回率 (Recall)**: 检索到的相关文件数 / 总相关文件数
- **命中率 (Hit Rate)**: 是否至少检索到一个相关文件 (1.0 或 0.0)
- **精确率 (Precision)**: 检索到的相关文件数 / 总检索文件数
- **答案质量 (Quality Score)**: 基于关键实体覆盖率和答案完整性的综合评分 (0.0-1.0)
- **实体覆盖率 (Entity Coverage)**: 答案中包含的期望关键实体比例
- **延迟 (Latency)**: 每个查询的平均响应时间 (毫秒)
- **Token 使用**: Prompt + Completion 的总 Token 数
