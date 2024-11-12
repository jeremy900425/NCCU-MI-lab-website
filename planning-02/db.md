## NoSQL 的 Schema

<img src="NoSQL.png" width="70%"/>

#### schema 說明
- user 會先登入，這邊會驗證相關的 API，驗證通過的話就進到他的個人頁面，在這邊可以主要有五項功能，包含檔案上傳、下載等等。
- 特別討論過的地方應該是因為我們想嘗試看看 Serverless 的架構，因此 Backend 那邊沒有寫 EC2，到時候應該會是 Call AWS 的 lambda 來達成我們想要的功能
