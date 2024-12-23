# 1. psycopg2 Issue
```
Traceback (most recent call last):
  File "/Users/chouchenyu/Desktop/nccucs/NCCU-MI-lab-website/login/accountCheck.py", line 1, in <module>
    import psycopg2
  File "/Users/chouchenyu/opt/anaconda3/envs/NCCU/lib/python3.11/site-packages/psycopg2/__init__.py", line 51, in <module>
    from psycopg2._psycopg import (                     # noqa
ImportError: dlopen(/Users/chouchenyu/opt/anaconda3/envs/NCCU/lib/python3.11/site-packages/psycopg2/_psycopg.cpython-311-darwin.so, 0x0002): symbol not found in flat namespace '_PQbackendPID'
```
## Solution
1. brew install postgresql
2. which pg_config
   出現 `/usr/local/bin/pg_config`
3. conda install -c conda-forge psycopg2
- 執行 conda install -c conda-forge psycopg2 成功的原因是 Conda 環境提供了一個完整且兼容的軟件依賴解決方案，以下是詳細解釋：