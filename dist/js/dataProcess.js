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

      var processedImageStr = response.data.processedImage;
      var processedImage = new Image();
      processedImage.src = "data:image/jpeg;base64," + processedImageStr;
      document.getElementById("resultContainer").appendChild(processedImage);
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
