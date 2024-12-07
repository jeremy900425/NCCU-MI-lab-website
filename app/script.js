document.getElementById('uploadButton').addEventListener('click', async () => {
    const apiUrl = 'https://6h82gw23ld.execute-api.us-east-1.amazonaws.com/default/FileUpload';
  
    try {
      const response = await fetch(apiUrl, {
        method: 'GET', // 改成 GET，如果 Lambda 需要
      });
  
      if (response.ok) {
        const result = await response.text(); // 假設回應是純文字 "Hello from Lambda!"
        alert(result); // 用 alert 顯示回應內容
      } else {
        alert('請求失敗，狀態碼：' + response.status);
      }
    } catch (error) {
      console.error('請求發生錯誤：', error);
      alert('請求發生錯誤，請查看主控台日誌。');
    }
  });
