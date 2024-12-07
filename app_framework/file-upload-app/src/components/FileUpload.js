import React from 'react';
import axios from 'axios';

const FileUpload = () => {
  const handleButtonClick = async () => {
    try {
      const response = await axios.get(
        'https://6h82gw23ld.execute-api.us-east-1.amazonaws.com/default/FileUpload'
      );
      alert(`API 回應：${response.data}`);
    } catch (error) {
      console.error('API 呼叫失敗', error);
      alert('API 呼叫失敗，請稍後再試');
    }
  };

  return (
    <div className="container mt-5 text-center">
      <button className="btn btn-primary" onClick={handleButtonClick}>
        呼叫 Lambda
      </button>
    </div>
  );
};

export default FileUpload;
