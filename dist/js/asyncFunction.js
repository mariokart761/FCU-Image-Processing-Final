// 顯示等待頁面
function showLoadingPage() {
  console.log("等待中...");
  // 顯示等待頁面的內容
}
function hideLoadingPage(imageData) {
  console.log("隱藏等待頁面");
  // 顯示結果頁面的內容，使用回傳的圖片資料
}
// 顯示結果頁面
function showResultPage(imageData) {
  console.log("顯示結果頁面");
  // 顯示結果頁面的內容，使用回傳的圖片資料
}

document
  .getElementById("sendButton")
  .addEventListener("click", async function () {
    try {
      // 顯示等待頁面
      showLoadingPage();

      const response = await axios.post("http://localhost:8000/api/image", {
        img_path: "./img/testImg.png",
        statusGaussianFilter: true,
        statusBrightnessFixMethod: "Clahe",
        statusSharpen: true,
        statusAdaptiveThreshold: true,
      });
      //   const formData = new FormData();
      //   const files = document.getElementById("formFile").files;
      //   const imgFile = files[0];
      //   formData.append("image", imgFile);
      //   formData.append("img_path", "./img/testImg.png");
      //   formData.append("statusGaussianFilter", true);
      //   formData.append("statusBrightnessFixMethod", "Clahe");
      //   formData.append("statusSharpen", true);
      //   formData.append("statusAdaptiveThreshold", true);

      //   const response = await axios.post(
      //     "http://localhost:8000/api/image",
      //     formData,
      //     {
      //       headers: {
      //         "Content-Type": "multipart/form-data",
      //       },
      //     }
      //   );

      console.log("response success!");

      // 隱藏等待頁面
      hideLoadingPage();

      var processedImageStr = response.data.processedImage;
      var processedImage = new Image();
      processedImage.src = "data:image/jpeg;base64," + processedImageStr;
      document.getElementById("resultContainer").appendChild(processedImage);

      // 顯示結果頁面
      showResultPage();
    } catch (error) {
      console.error(error);
    }
  });

function readFileAsBuffer(file) {
  const reader = new FileReader();
  reader.readAsArrayBuffer(file);
  return new Promise((resolve) => {
    reader.onload = () => resolve(reader.result);
  });
}
async function handleImageFile(event) {
  const { files } = event.target;
  const imgFile = files[0];
  const imgBuffer = await readFileAsBuffer(files[0]);
  const previewURL = URL.createObjectURL(
    new Blob([imgBuffer], { type: "image/jpeg" })
  );
  $("#previewImage").attr("src", previewURL);

  // 建立 FormData 物件
  const formData = new FormData();
  formData.append("image", imgFile);
}
