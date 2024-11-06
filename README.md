# 詳細功能

## 檔案上傳
- 詳細功能：使用者可以將檔案上傳到系統中，支援多檔案上傳及進度顯示。
- 系統運作：
    - 使用 AWS S3 作為主要的文件儲存的地方。
    - 前端可以使用 AWS SDK for JavaScript 與 S3 進行直接的檔案上傳。後端可以使用 Amazon API Gateway 和 AWS Lambda 組合來處理驗證並為檔案生成臨時的 URL，以便安全地進行上傳。
    - 使用 AWS S3 Transfer Acceleration 提高大檔案的上傳速度。
- 資料流：
  - API Gateway 觸發 AWS Lambda 函數生成臨時的 URL，並基於使用者的身份和權限設定限制。
  - Lambda 將臨時的 URL 回傳給前端。
  - 前端使用這個 URL，直接將檔案上傳到 Amazon S3。
  - S3 儲存檔案後，將上傳完成的通知（event）發送給 EventBridge 或透過 Lambda 進行處理（例如將檔案路徑存入 AWS RDS 供日後查詢）。
  - 用戶收到上傳成功的訊息並查看文件列表中的新檔案。
## 檔案下載
- 詳細功能：允許使用者下載他們已上傳的檔案，並且可以管理不同的下載權限。
- 系統運作：
  - 透過 S3 提供的 臨時的 URL 功能生成限時的下載連結。
  - 使用 Amazon CloudFront 作為 CDN，加速全球使用者的下載速度。
  - 利用 IAM 設置下載權限，以確保只有授權的使用者能夠下載檔案。
- 資料流：
    - 前端向 API Gateway 發出請求，要求生成一個下載的臨時的 URL。
    - API Gateway 觸發 AWS Lambda，Lambda 驗證使用者的身份和下載權限。
    - 如果有權限，Lambda 創建一個下載臨時的 URL 並回傳至前端。
    - 前端使用此 URL 直接從 Amazon S3 下載檔案。
    - Amazon CloudFront 作為 CDN 加速使用者的檔案下載。
## 檔案刪除
- 詳細功能：使用者可以永久刪除他們的檔案，並支援垃圾桶功能（例如：將檔案先移到垃圾桶，保留30天）。
- 系統運作：
  - 使用 S3 Lifecycle Policies 設定垃圾桶管理，在刪除前將檔案移動到指定的 S3 資料夾中。
  - 在30天後自動刪除檔案或通過 Lambda 函數實現定時刪除。
  - 使用 S3 Object Versioning 防止意外刪除，保留檔案的多個版本供恢復使用。
- 資料流：
    - 前端向 API Gateway 發出刪除請求。
    - API Gateway 觸發 AWS Lambda，Lambda 檢查用戶的刪除權限。
    - 如果允許刪除，Lambda 調用 S3 Delete Object API 將檔案移至垃圾桶資料夾（設定在 S3 Lifecycle Policies 中，垃圾桶內檔案將在30天後自動刪除）。
    - Lambda 更新 RDS 中的資料庫紀錄，反映刪除狀態。
    - 用戶的檔案列表中顯示檔案已刪除。
## 檔案預覽
- 詳細功能：支援多種檔案類型（如 PDF、圖片、文字檔）的檔案預覽，無需下載檔案即可查看內容。
- 系統運作：
  - 使用 Amazon S3 和 Amazon CloudFront 提供圖片和文件的預覽連結。
  - 使用 AWS Lambda 和 Amazon API Gateway 進行文件轉換，例如將 PDF 文件轉為圖片預覽。
  - 對於視頻文件，可以使用 Amazon Elastic Transcoder 或 AWS Elemental MediaConvert 進行格式轉換以適應不同的設備預覽需求。
- 資料流：
    - 前端向 API Gateway 發送請求，要求預覽文件。
    - API Gateway 觸發 AWS Lambda 函數，Lambda 根據檔案類型（如 PDF、圖片或視頻）進行不同處理。
    - 如果是圖片或 PDF，Lambda 直接返回 S3 臨時的 URL，允許前端載入文件。
    - 若為視頻檔案，Lambda 使用 Amazon Elastic Transcoder 或 MediaConvert 將視頻轉換為合適格式（如低解析度預覽）。
    - 前端使用 CloudFront 或 S3 提供的 URL 顯示預覽畫面。
## 檔案共享權限優化
- 詳細功能：允許使用者設定檔案的共享權限，例如僅供閱讀、編輯或下載。
- 系統運作：
  - 使用 IAM 角色和政策 來管理不同的檔案存取權限，根據角色設定不同的權限。
  - 使用 Amazon Cognito 管理使用者身份驗證，並根據使用者角色分配不同的權限。
  - 使用 Lambda 檢查使用者的權限，確保只有擁有權限的使用者能夠訪問相應的檔案。
- 資料流：
    - 前端向 API Gateway 發送設置權限的請求。
    - API Gateway 觸發 AWS Lambda，Lambda 根據用戶設定的共享選項生成 IAM 角色和政策。
    - 使用 Amazon Cognito 將使用者和共用者的身份驗證資訊記錄，並在 RDS 更新共享權限。
    - 當共用者嘗試訪問文件時，Lambda 驗證其權限並生成相應的臨時的 URL 或拒絕訪問。
    - 如果權限允許，前端獲得訪問 URL 並能夠執行檔案操作（例如查看、編輯或下載）。