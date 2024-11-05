# 各功能詳細說明

## 檔案上傳
#### 功能說明：
- 此功能允許使用者將檔案上傳至雲端儲存，並透過我們的服務進行管理。上傳的檔案將會儲存在AWS S3中。
#### 使用方式：
1. 使用者必須先登入系統並通過授權驗證。
2. 登入成功後，進入檔案管理界面並選擇「上傳」按鈕。
3. 使用者選擇本地檔案後，即可啟動上傳流程，檔案會被儲存至S3，會看到上傳進度條，顯示當前的上傳進度百分比。
4. 當上傳完成後，系統將立即顯示上傳成功的通知，以確認檔案已成功儲存。
5. 上傳完成的檔案會即時顯示於使用者介面中，包含檔案名稱、上傳時間、檔案大小等詳細資訊
#### 資料流：
1. 使用者登入系統
   - 動作：使用者進入登入頁面，輸入帳號與密碼。 
   - 系統處理：
     - 透過 **AWS Cognito API** 進行身份驗證。
     - 成功登入後，系統生成和返回一個 **JWT(或其他)**，以供後續請求驗證。
   - 後續行為：登入成功，使用者被引導至檔案管理頁面。

2. 使用者查看檔案列表
   - 動作：使用者進入檔案管理頁面。
   - 系統處理：
     - Client 發送 **檔案列表 API** 請求至後端，以取得該使用者上傳的所有檔案的 meta data（如檔案名稱、大小、上傳日期、狀態等）。

3. 進入檔案管理介面並選擇「上傳」
   - 動作：使用者進入檔案管理介面，選擇「上傳」按鈕以選擇本地檔案。
   - 系統處理：
     - Client 端將檔案上傳請求發送至 **檔案上傳 API**，後端生成 S3 簽名網址 (Presigned URL)，並返回給 Client。
     - Client 使用此 URL 直接將檔案上傳至 S3，此過程中可以透過事件監聽顯示上傳進度條，更新上傳百分比。

4. 上傳完成通知
   - 系統處理：
     - Client 再次請求 **更新檔案 meta data API**，將上傳完成的檔案資訊（如檔案名稱、大小、上傳時間等）儲存在 RDS 的 meta data 中。
     - 後端更新 meta data 後返回成功訊息給 Client，通知上傳成功。

5. 即時更新介面
   - 系統處理：
     - Client 收到後端返回的成功訊息後，即時更新使用者介面，顯示新上傳檔案的詳細資訊。
     - 使用者可以看到上傳檔案的名稱、大小、上傳時間等，確認檔案已成功儲存至 S3 並在介面中顯示。


#### 可能使用到的 API：
*上傳檔案原則：先透過 檔案上傳 API 請求 生成 Presigned URL API 後才會得到 URL，檔案上傳 API 回傳這個 URL 就可以上傳檔案*
| API 名稱                   | 主要用途                        | 使用說明                             |
|----------------------------|--------------------------------|--------------------------------------|
| AWS Cognito Auth API       | 使用者登入、驗證               | 驗證身份並生成 JWT                   |
| AWS S3 Presigned URL       | 生成簽名網址                   | 允許直接上傳檔案至 S3                |
| 檔案列表 API               | 取得檔案列表                  | 從 RDS 查詢使用者的檔案 meta data     |
| 檔案上傳 API               | 生成上傳用的簽名網址          | 驗證身份，返回 S3 Presigned URL       |
| 更新檔案 meta data API     | 儲存上傳完成的檔案資訊         | 上傳完成後，將檔案 meta data 存入 RDS |
| 通知 API           | 回報上傳狀態                  | 上傳成功或失敗通知，更新使用者介面    |

---
## 檔案刪除
#### 功能描述：
此功能允許使用者刪除雲端儲存中的檔案，刪除後的檔案會移至「垃圾桶」中，並保留30天，方便誤刪後還原。每個檔案在垃圾桶中會顯示剩餘天數，並在30天後自動永久刪除。
#### 使用方式：
1. 使用者登入後，在檔案管理界面中可以查看既有的檔案，並在每個檔案右側看到垃圾桶圖示。
2. 點擊垃圾桶圖示後，系統將彈出確認視窗，詢問使用者是否要將檔案刪除至垃圾桶。
3. 點擊「是」後，檔案從檔案列表中消失並移至垃圾桶。
4. 使用者可以在垃圾桶中查看已刪除的檔案，每個檔案會顯示剩餘的保留天數，過期後會自動刪除。
#### 資料流
1. 使用者登入系統
   - 動作：使用者進入登入頁面，輸入帳號與密碼。 
   - 系統處理：
     - 透過 **AWS Cognito API** 進行身份驗證。
     - 成功登入後，系統生成和返回一個 **JWT(或其他)**，以供後續請求驗證。
   - 後續行為：登入成功，使用者被引導至檔案管理頁面。
2. 使用者查看檔案列表
   - 動作：使用者進入檔案管理頁面。
   - 系統處理：
     - Client 發送 **檔案列表 API** 請求至後端，以取得該使用者上傳的所有檔案的 meta data（如檔案名稱、大小、上傳日期、狀態等）。
3. 使用者點擊垃圾桶圖示
   - 系統處理：
        - 系統彈出確認刪除的視窗，詢問是否要刪除檔案至垃圾桶。
4. 使用者確認刪除檔案
   - 動作：使用者點擊「是」以確認刪除檔案。
   - 系統處理：
        - 客戶端發送 **刪除檔案 API** 請求至後端，請求內容包括檔案ID和使用者的token。
       - 後端檢查token是否有效，並驗證使用者對該檔案的刪除權限。
       - 成功驗證後，後端更新 RDS 中的 meta data，將檔案狀態標記為「垃圾桶」，並記錄刪除日期。
       - AWS S3 將檔案移至「垃圾桶」資料夾中，確保檔案不再顯示於主檔案列表。
      - 通知 API 返回刪除成功訊息給客戶端，並更新檔案管理介面，移除該檔案。
5. 檔案在垃圾桶中顯示剩餘天數
    - 動作：使用者在垃圾桶介面查看刪除的檔案。
    - 系統處理：
      - 客戶端發送 **垃圾桶檔案列表 API** 請求，以查詢所有刪除且尚未永久刪除的檔案。
      - 後端從 RDS 中提取檔案資訊，包含檔案ID、名稱、刪除日期等。
      - 使用者界面根據檔案的刪除日期計算剩餘天數，並即時顯示於垃圾桶介面。
6. Lambda 定期清理垃圾桶檔案
   - 動作：系統每日觸發自動清理程序。
   - 系統處理：
     - AWS Lambda 定期（每日）掃描 RDS，檢查垃圾桶中的檔案是否超過30天。
     - 對於超過30天的檔案，Lambda 調用 AWS S3 API 永久刪除該檔案，並更新 RDS 將相應檔案紀錄標記為已刪除。
     - 刪除後，系統不再在垃圾桶介面顯示該檔案。
#### 此功能預計使用的API
| API 名稱                    | 主要用途                              | 使用說明                                                                 |
|-----------------------------|---------------------------------------|--------------------------------------------------------------------------|
| AWS Cognito Auth API        | 使用者登入與身份驗證                 | 驗證使用者身份並生成 JWT Token                                          |
| 檔案列表 API                | 取得檔案列表                          | 查詢使用者上傳的所有檔案 meta data，包含檔案名稱、大小、上傳日期等       |
| 刪除檔案 API                | 刪除檔案至垃圾桶                      | 檢查 JWT Token，驗證刪除權限後，更新 RDS 的檔案狀態為「垃圾桶」         |
| AWS S3 Move Object API      | 移動檔案至垃圾桶資料夾                | 將檔案從主資料夾移至「垃圾桶」資料夾，避免在主檔案列表中顯示             |
| 通知 API                    | 刪除操作通知                          | 返回刪除成功訊息至前端，更新檔案管理介面                                  |
| 垃圾桶檔案列表 API          | 查詢垃圾桶中的檔案列表                | 從 RDS 查詢所有被刪除但未永久刪除的檔案資訊，包含刪除日期等             |
| AWS Lambda 定期清理 API      | 定期清理垃圾桶中超過30天的檔案       | 使用 AWS Lambda 每日掃描 RDS，刪除垃圾桶中超過30天的檔案，並更新 RDS     |
| AWS S3 Delete Object API    | 永久刪除 S3 中的檔案                 | Lambda 調用該 API 永久刪除超過30天的檔案，並更新 RDS 將記錄標記為已刪除 |

---
## 預覽檔案
#### 功能說明
此功能允許使用者在檔案管理界面中，雙擊檔案以快速預覽檔案的內容。當檔案類型為圖片、PDF、或文字檔案時，系統將以視覺化方式顯示該檔案的內容。對於無法直接預覽的檔案類型，會顯示檔案資訊和提示。
#### 使用方式
1. 使用者登入系統並進入檔案管理界面。
2. 在檔案列表中，使用者雙擊任一檔案（如圖片、PDF、或文字檔案）。
3. 系統即時顯示該檔案的預覽，允許使用者快速查看內容。
4. 預覽完成後，使用者可以關閉預覽界面返回檔案列表。
#### 資料流
1. 使用者登入並進入檔案管理界面：
   - 動作：使用者登入後，進入檔案管理頁面。
   - 系統處理：使用 Cognito API 進行身份驗證，並展示該使用者的檔案列表。
2. 使用者雙擊檔案進行預覽：
   - 動作：使用者在檔案列表中雙擊檔案以進行預覽。
   - 系統處理：
     - Client 發送 請求預覽 API 至後端，請求內容包括檔案 ID 和使用者的 Token。
     - 後端檢查 Token 是否有效並驗證使用者的檔案預覽權限。
     - 成功驗證後，後端生成或請求該檔案的 S3 簽名網址 (Presigned URL)，返回給 Client。
3. Client 使用 Presigned URL 獲取檔案內容：
   - 系統處理：
     - Client 使用取得的 Presigned URL 從 S3 獲取檔案內容。
     - 如果檔案為圖片或 PDF，Client 直接顯示於預覽界面中；如果為文字檔案，Client 解析後顯示其內容。
     - 對於無法預覽的檔案類型，Client 顯示提示訊息。
4. 預覽結束並關閉視窗：
   - 動作：使用者預覽完畢後關閉視窗，回到檔案管理頁面。
   - 系統處理：Client 結束檔案讀取，釋放相關資源。
#### 可能使用到的API
| API 名稱                    | 主要用途                              | 使用說明                                                                 |
|-----------------------------|---------------------------------------|--------------------------------------------------------------------------|
| AWS Cognito Auth API        | 使用者登入與身份驗證                 | 確保使用者具備預覽檔案的權限                                            |
| 檔案列表 API                | 取得檔案列表                          | 查詢使用者上傳的檔案 meta data（如名稱、大小、類型等）                    |
| 請求預覽 API                | 請求預覽檔案                          | 驗證 JWT Token，確認使用者對檔案的預覽權限，並生成 S3 簽名網址            |
| AWS S3 Presigned URL        | 生成預覽用的簽名網址                 | 允許 Client 透過 URL 存取檔案內容進行預覽                                 |
---

