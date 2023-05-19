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

      const data = new FormData();
      data.append('img_content', imageData); 
      data.append('statusGaussianFilter', true);
      data.append('statusBrightnessFixMethod', 'Clahe');
      data.append('statusSharpen', true);
      data.append('statusAdaptiveThreshold', true);
      console.log(data)

      // 顯示等待頁面
      showLoadingPage();

      const response = await axios.post("/api/image", data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

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
let imageData;
async function handleImageFile(event) {
  const { files } = event.target;
  const file = files[0];
  const imgBuffer = await readFileAsBuffer(file);
  const previewURL = URL.createObjectURL(
    new Blob([imgBuffer], { type: "image/jpeg" })
  );
  $("#previewImage").attr("src", previewURL);
  imageData = file;
}
