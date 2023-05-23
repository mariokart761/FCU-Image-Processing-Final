class DataProcessor {
  constructor() {
    this._imageData = null;
    this._statusGaussianFilter = true;
    this._statusBrightnessFixMethod = '0';
    this._statusUnsharpMasking = true;
    this._statusAdaptiveThreshold = true;
    this._statusExperiment = '0';
    this._statusBrightAdj = 0;
  }

  get imageData() {
    return this._imageData;
  }
  set imageData(newValue) {
    this._imageData = newValue;
  }

  get statusGaussianFilter() {
    return this._statusGaussianFilter;
  }
  set statusGaussianFilter(newValue) {
    this._statusGaussianFilter = newValue;
  }

  get statusBrightnessFixMethod() {
    return this._statusBrightnessFixMethod;
  }
  set statusBrightnessFixMethod(newValue) {
    this._statusBrightnessFixMethod = newValue;
  }

  get statusUnsharpMasking() {
    return this._statusUnsharpMasking;
  }
  set statusUnsharpMasking(newValue) {
    this._statusUnsharpMasking = newValue;
  }

  get statusAdaptiveThreshold() {
    return this._statusAdaptiveThreshold;
  }
  set statusAdaptiveThreshold(newValue) {
    this._statusAdaptiveThreshold = newValue;
  }

  get statusExperiment() {
    return this._statusExperiment;
  }
  set statusExperiment(newValue) {
    this._statusExperiment = newValue;
  }

  get statusBrightAdj() {
    return this._statusBrightAdj;
  }
  set statusBrightAdj(newValue) {
    this._statusBrightAdj = newValue;
  }
}
const dataProcessor = new DataProcessor();

// 將Base64轉為Blob圖像
function base64ToBlob(base64, contentType) {
  var byteCharacters = atob(base64);
  var byteArrays = [];

  var sliceSize = 1024;
  var offset = 0;

  while (offset < byteCharacters.length) {
    var slice = byteCharacters.slice(offset, offset + sliceSize);
    var byteNumbers = new Array(slice.length);

    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    var byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);

    offset += sliceSize;
  }

  return new Blob(byteArrays, { type: contentType });
}



document
  .getElementById("sendButton")
  .addEventListener("click", async function () {
    try {
      if(checkSettingInput()!=true) return;

      const formData = new FormData();
      formData.append('img_content', dataProcessor.imageData); 
      formData.append('statusGaussianFilter', dataProcessor.statusGaussianFilter);
      formData.append('statusBrightnessFixMethod', dataProcessor.statusBrightnessFixMethod);
      formData.append('statusSharpen', dataProcessor.statusUnsharpMasking);
      formData.append('statusAdaptiveThreshold', dataProcessor.statusAdaptiveThreshold);
      formData.append('statusExperiment', dataProcessor.statusExperiment);
      formData.append('statusBrightAdj', dataProcessor.statusBrightAdj);
      console.log(formData)

      // 顯示等待頁面
      showLoadingPage();

      const response = await axios.post("/api/orbProcessing", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if(dataProcessor.statusExperiment === 'exp1'){
      }
      else if(dataProcessor.statusExperiment === 'exp2'){
        console.log("Exp2 response success!");
        var contentType = 'image/jpg';
        var resultImageLeft = response.data.processedImageLeft;
        var resultImageRight = response.data.processedImageRight;
        var resultImageMatch = response.data.processedImageMatch;
        var blobResultImgLeft = base64ToBlob(resultImageLeft, contentType);
        var blobResultImgRight = base64ToBlob(resultImageRight, contentType);
        var blobResultImgMatch = base64ToBlob(resultImageMatch, contentType);
        var resultImgLeftUrl = URL.createObjectURL(blobResultImgLeft);
        var resultImgRightUrl = URL.createObjectURL(blobResultImgRight);
        var resultImgMatchUrl = URL.createObjectURL(blobResultImgMatch);

        $("#resultImage").attr("src", resultImgLeftUrl);

        var keypointNumLeft = response.data.keypointNumLeft;
        var detectTimeLeft = response.data.detectTimeLeft;
        $$("#keypoint-left-num").innerHTML = keypointNumLeft;
        $$("#time-left-num").innerHTML = detectTimeLeft + " s";
        // console.log(keypointNum)
        // console.log(detectTime)

        // 顯示結果頁面
        showResultPage();
      }
      else if(dataProcessor.statusExperiment === 'exp3'){
        console.log("Exp3 response success!");
        var contentType = 'image/jpg';
        var resultImage = response.data.processedImage;
        var blobResultImg = base64ToBlob(resultImage, contentType);
        var resultImgUrl = URL.createObjectURL(blobResultImg);
        $("#resultImage").attr("src", resultImgUrl);

        var keypointNum = response.data.keypointNum;
        var detectTime = response.data.detectTime;
        $$("#keypoint-left-num").innerHTML = keypointNum;
        $$("#time-left-num").innerHTML = detectTime + " s";
        // console.log(keypointNum)
        // console.log(detectTime)

        // 顯示結果頁面
        showResultPage();
      }
    } catch (error) {
      console.error(error);
    }
  });

// 將file圖像轉為buffer
function readFileAsBuffer(file) {
  const reader = new FileReader();
  reader.readAsArrayBuffer(file);
  return new Promise((resolve) => {
    reader.onload = () => resolve(reader.result);
  });
}

// 將選擇的檔案以Blob型式顯示在$("#previewImage")中
async function handlePreviewImageFile(event) {
  const { files } = event.target;
  const file = files[0];
  const imgBuffer = await readFileAsBuffer(file);
  const previewURL = URL.createObjectURL(
    new Blob([imgBuffer], { type: "image/jpeg" })
  );
  $("#previewImage").attr("src", previewURL);
  dataProcessor.imageData = file;
}
