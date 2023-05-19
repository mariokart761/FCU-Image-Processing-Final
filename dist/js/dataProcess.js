class DataProcessor {
  constructor() {
    this._imageData = null;
    this._statusGaussianFilter = true;
    this._statusBrightnessFixMethod = true;
    this._statusAdaptiveThreshold = true;
    this._statusExperiment = true;
    this._statusBrightAdj = 0;
  }
  // Getter
  get imageData() {
    return this._imageData;
  }

  // Setter
  set imageData(newValue) {
    this._imageData = newValue;
  }
}
const dataProcessor = new DataProcessor();

// 将Base64图像数据转换为Blob对象
function base64ToBlob(base64Data, contentType) {
  var sliceSize = 1024;
  var byteCharacters = atob(base64Data);
  var byteArrays = [];
  for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    var slice = byteCharacters.slice(offset, offset + sliceSize);
    var byteNumbers = new Array(slice.length);
    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }
    var byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);
  }
  var blob = new Blob(byteArrays, { type: contentType });
  return blob;
}

document
  .getElementById("sendButton")
  .addEventListener("click", async function () {
    try {
      if(checkSettingInput()!=true) return;
      const data = new FormData();
      data.append('img_content', dataProcessor.imageData); 
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
      var contentType = 'image/jpg';
      var resultImage = response.data.processedImage;
      var blobResultImg = base64ToBlob(resultImage, contentType);
      var resultImgUrl = URL.createObjectURL(blobResultImg);
      $("#resultImage").attr("src", resultImgUrl);

      var keypointNum = response.data.keypointNum;
      var detectTime = response.data.detectTime;
      console.log(keypointNum)
      console.log(detectTime)

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
  const file = files[0];
  const imgBuffer = await readFileAsBuffer(file);
  const previewURL = URL.createObjectURL(
    new Blob([imgBuffer], { type: "image/jpeg" })
  );
  $("#previewImage").attr("src", previewURL);
  dataProcessor.imageData = file;
}
